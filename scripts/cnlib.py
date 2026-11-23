"""Inventory and transport for the four-Mac lab."""
from contextlib import contextmanager
import fcntl
import ipaddress
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NODES = ("mac1", "mac2", "mac3", "mac4")
ROLES = {
    "mac1": ("dns",),
    "mac2": ("dns", "edge"),
    "mac3": ("edge", "backend"),
    "mac4": ("backend",),
}
SSH = ("ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
       "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no",
       "-o", "ClearAllForwardings=yes", "-o", "ForwardAgent=no")


def run(args, *, data=None, check=True, display=False, timeout=90):
    args = list(map(str, args))
    if display:
        print("$ " + shlex.join(args), flush=True)
    result = subprocess.run(args, input=data, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=timeout)
    if display or (check and result.returncode):
        print(result.stdout, end="", flush=True)
        print(result.stderr, end="", file=sys.stderr, flush=True)
    if check:
        result.check_returncode()
    return result


class Lab:
    def __init__(self, file=None):
        path = Path(file or os.environ.get("CN_INVENTORY", ROOT / "team/team.env"))
        self.env = {}
        for line in path.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                key, value = line.split("=", 1)
                if key in self.env:
                    raise ValueError(f"Duplicate inventory key {key}")
                self.env[key] = value.strip()
        expected = {"DOMAIN", "LAN", "GATEWAY", "INTERFACE", "TTL", "UPSTREAM_DNS",
                    "PORT_A", "PORT_B", *(node.upper() for node in NODES)}
        if self.env.keys() != expected:
            raise ValueError(f"Inventory keys missing or unexpected: {self.env.keys() ^ expected}")
        self.domain = self.env["DOMAIN"]
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.test", self.domain):
            raise ValueError("DOMAIN must be a single private label under .test")
        self.app, self.api = (f"{name}.{self.domain}" for name in ("app", "api"))
        self.network = ipaddress.IPv4Network(self.env["LAN"])
        self.gateway = ipaddress.IPv4Address(self.env["GATEWAY"])
        self.interface = self.env["INTERFACE"]
        self.ttl = int(self.env["TTL"])
        self.ports = {name: int(self.env[f"PORT_{name}"]) for name in ("A", "B")}
        self.upstreams = [ipaddress.IPv4Address(ip) for ip in self.env["UPSTREAM_DNS"].split()]
        self.users, self.ips = {}, {}
        for node in NODES:
            user, ip = self.env[node.upper()].split("@")
            if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_-]*", user):
                raise ValueError(f"Invalid user for {node}")
            address = ipaddress.IPv4Address(ip)
            if address not in self.network or address in (self.network.broadcast_address,
                    self.network.network_address, self.gateway) or ip in self.ips.values():
                raise ValueError(f"Invalid or duplicate LAN address for {node}: {ip}")
            self.users[node], self.ips[node] = user, ip
        if (self.gateway not in self.network or not re.fullmatch(r"en[0-9]+", self.interface)
                or self.ttl != 30 or len(set(self.ports.values())) != 2
                or any(not 1024 <= p < 65536 for p in self.ports.values())
                or not self.upstreams or any(str(ip) in self.ips.values() for ip in self.upstreams)):
            raise ValueError("Invalid interface, gateway, TTL, backend ports or upstream DNS")

    def on(self, node, args, **kwargs):
        args = list(map(str, args))
        if node == "mac1":
            return run(args, **kwargs)
        return run((*SSH, self.env[node.upper()], shlex.join(args)), **kwargs)

    def runtime(self, node):
        return Path(f"/Users/{self.users[node]}/cn-project")

    def node(self, node, *args, **kwargs):
        return self.on(node, (self.runtime(node) / "bin/node.sh", *args), **kwargs)

    def query(self, node, name, *, source="mac1", tcp=False):
        args = ["dig", f"@{self.ips[node]}", name, "A", "+time=2", "+tries=1", "+noall", "+answer"]
        if tcp:
            args.append("+tcp")
        result = self.on(source, args, check=False, timeout=10)
        return [(int(fields[1]), fields[4]) for line in result.stdout.splitlines()
                if len(fields := line.split()) == 5 and fields[3] == "A"]

    def https(self, hostname, *, source="mac1", ip=None, path="/api/status", extra=(), **kwargs):
        args = ["curl", "--noproxy", "*", "--http1.1", "-sS", "--connect-timeout", "3",
                "--max-time", "8", "-D", "-", "-o", "/dev/null"]
        if ip:
            args.extend(("--resolve", f"{hostname}:443:{ip}"))
        return self.on(source, (*args, *extra, f"https://{hostname}{path}"), **kwargs)


def headers(response):
    lines = response.stdout.splitlines()
    if not lines or not lines[0].startswith("HTTP/"):
        raise RuntimeError(response.stderr.strip() or "Missing HTTP response")
    return int(lines[0].split()[1]), {
        key.lower(): value.strip()
        for line in lines[1:] if ":" in line
        for key, value in [line.split(":", 1)]
    }


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@contextmanager
def operation_lock(*, allow_fault=False):
    """Serialize controller-side changes while allowing individual read-only SSH probes."""
    with (ROOT / "team/.operation.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("Another deployment or demo is running on Mac 1") from error
        require(allow_fault or not (ROOT / "team/.demo-state.json").exists(),
                "A practice fault is active. Run ./scripts/demo.sh fix first.")
        yield
