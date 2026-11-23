"""Non-mutating HTTP/1.1, DNS, trust, cache and round-robin assertions."""
from cnlib import Lab, headers, require


def series(lab, edge, ip=None, *, only=None, source="mac1", count=6):
    actual = []
    for _ in range(count):
        result = lab.https(lab.app, ip=ip, source=source, display=True)
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


def smoke(lab):
    for node in ("mac1", "mac2"):
        for name in (lab.app, lab.api):
            for tcp in (False, True):
                answers = lab.query(node, name, tcp=tcp)
                print(f"{node} DNS {'TCP' if tcp else 'UDP'} {name}: {answers}")
                require(answers == [(lab.ttl, lab.ips["mac2"])], f"Unexpected {node} DNS answer")
    series(lab, "edge1-mac2")
    series(lab, "edge2-mac3", lab.ips["mac3"])
    for source in ("mac1", "mac4"):
        status, fields = headers(lab.https(lab.api, source=source, display=True))
        require(status == 200 and fields.get("x-edge") == "edge1-mac2", f"{source} API path failed")
    for node in ("mac2", "mac3"):
        for hostname in (lab.app, lab.api):
            response = lab.on("mac1", ("curl", "--noproxy", "*", "-sS", "--max-time", "5",
                "--resolve", f"{hostname}:80:{lab.ips[node]}", "-D", "-", "-o", "/dev/null",
                f"http://{hostname}/"), display=True)
            code, fields = headers(response)
            require(code == 301 and fields.get("location") == f"https://{hostname}/",
                    f"HTTP redirect mismatch for {node}/{hostname}")
    status, fields = headers(lab.https(lab.app, path="/api/cache", display=True))
    tag = fields.get("etag")
    require(status == 200 and tag and "max-age=60" in fields.get("cache-control", ""), "Missing cache headers")
    code, _ = headers(lab.https(lab.app, path="/api/cache", extra=("-H", f"If-None-Match: {tag}"), display=True))
    require(code == 304, "Expected HTTP 304")


if __name__ == "__main__":
    smoke(Lab())
