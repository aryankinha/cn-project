"""Non-mutating HTTP/1.1, DNS, trust, cache and round-robin assertions."""
from cnlib import Lab, headers, require


def series(lab, edge, ip=None, *, only=None, source="mac1", count=6, verbose=True):
    actual = []
    for _ in range(count):
        result = lab.https(lab.app, ip=ip, source=source, display=verbose)
        code, fields = headers(result)
        require(result.stdout.startswith("HTTP/1.1 200") and code == 200 and
                fields.get("x-edge") == edge, f"Expected HTTP/1.1 200 and {edge}")
        actual.append(fields.get("x-backend"))
    if only:
        require(actual == [only] * count, f"Expected only {only}, got {actual}")
    else:
        require(set(actual) == {"A", "B"} and all(a != b for a, b in zip(actual, actual[1:])),
                f"Expected rotating A/B, got {actual}")
    print(f"{edge} backend series: {' '.join(actual)}")


def smoke(lab, *, verbose=True):
    primary = lab.ips["mac2"]
    for node in ("mac1", "mac2"):
        for name in (lab.app, lab.api):
            for tcp in (False, True):
                transport = "TCP" if tcp else "UDP"
                answers = lab.query(node, name, tcp=tcp)
                if verbose:
                    print(f"{node} DNS {transport} {name}: {answers}")
                require(answers == [(lab.ttl, primary)],
                        f"{node} DNS {transport} {name} returned {answers}; expected {primary}, TTL {lab.ttl}")
        if not verbose:
            print(f"{node} DNS: both names point to {primary} over UDP/TCP (TTL {lab.ttl}s)")
    series(lab, "edge1-mac2", verbose=verbose)
    series(lab, "edge2-mac3", lab.ips["mac3"], verbose=verbose)
    for source in ("mac1", "mac4"):
        status, fields = headers(lab.https(lab.api, source=source, display=verbose))
        require(status == 200 and fields.get("x-edge") == "edge1-mac2", f"{source} API path failed")
        if not verbose:
            print(f"{source}: trusted HTTP/1.1 {status} for {lab.api}")
    for node in ("mac2", "mac3"):
        for hostname in (lab.app, lab.api):
            response = lab.on("mac1", ("curl", "--noproxy", "*", "-sS", "--max-time", "5",
                "--resolve", f"{hostname}:80:{lab.ips[node]}", "-D", "-", "-o", "/dev/null",
                f"http://{hostname}/"), display=verbose)
            code, fields = headers(response)
            require(code == 301 and fields.get("location") == f"https://{hostname}/",
                    f"HTTP redirect mismatch for {node}/{hostname}")
    status, fields = headers(lab.https(lab.app, path="/api/cache", display=verbose))
    tag = fields.get("etag")
    require(status == 200 and tag and "max-age=60" in fields.get("cache-control", ""), "Missing cache headers")
    code, _ = headers(lab.https(lab.app, path="/api/cache", extra=("-H", f"If-None-Match: {tag}"), display=verbose))
    require(code == 304, "Expected HTTP 304")
    if not verbose:
        print("Both edges: HTTP 301 redirects for both names")
        print(f"Cache: {fields['cache-control']} · ETag {tag} · HTTP {code}")


if __name__ == "__main__":
    smoke(Lab())
