"""Render role-specific files without embedding credentials or private keys."""
import argparse
from pathlib import Path
from string import Template

from cnlib import Lab, NODES, ROLES, ROOT


def render(lab, node, dest):
    home = lab.runtime(node)
    backend = {"mac3": "A", "mac4": "B"}.get(node, "")
    edge = {"mac2": "edge1-mac2", "mac3": "edge2-mac3"}.get(node, "")

    def put(path, body):
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)

    def config(source, target, **fields):
        template = Template((ROOT / source).read_text())
        put(target, template.substitute(home=home, **fields))

    put("node.env", "\n".join((
        f"NODE={node}", f"ROLES='{' '.join(ROLES[node])}'", f"DOMAIN={lab.domain}",
        f"EDGE_ID={edge}", f"BACKEND_ID={backend}",
        f"BACKEND_PORT={lab.ports.get(backend, '')}", "",
    )))
    for script in ("node.sh", "phase2/firewall.sh", "phase2/client.sh"):
        put(f"bin/{Path(script).name}", (ROOT / "scripts" / script).read_text())

    if "dns" in ROLES[node]:
        config("dnsmasq/phase2.conf.template", "dnsmasq/dnsmasq.conf",
               domain=lab.domain, ttl=lab.ttl,
               upstreams="\n".join(f"server={ip}" for ip in lab.upstreams))
        put("dnsmasq/project.hosts", "".join(
            f"{lab.ips['mac2']} {host}\n" for host in (lab.app, lab.api)))

    if "edge" in ROLES[node]:
        config("nginx/phase2-master.conf.template", "nginx/nginx.conf", site="cn-project.conf")
        config("nginx/phase2-site.conf.template", "nginx/cn-project.conf",
               app=lab.app, api=lab.api, edge=edge,
               backend_a=f"{'127.0.0.1' if node == 'mac3' else lab.ips['mac3']}:{lab.ports['A']}",
               backend_b=f"{lab.ips['mac4']}:{lab.ports['B']}")

    if backend:
        for name in ("app.py", "requirements.txt"):
            put(f"backend/{name}", (ROOT / "backend" / name).read_text())
        for profile in ("strict", "standby"):
            edges = lab.ips["mac2"]
            if profile == "standby" and backend == "B":
                edges = "{ " + edges + ", " + lab.ips["mac3"] + " }"
            port = lab.ports[backend]
            config("firewall/backend.pf.template", f"firewall/{profile}.pf",
                   loopback=f"pass in quick on lo0 proto tcp to port {port}" if backend == "A" else "",
                   edges=edges, ip=lab.ips[node], port=port, interface=lab.interface)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    for name in NODES:
        render(Lab(), name, args.directory / name)
