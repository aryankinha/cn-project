# Private DNS — Aryan Kinha, Mac 1

Private IP: `10.7.23.16`; DNS UDP/TCP port 53. Both `app.team.test` and `api.team.test` map to Divyanshu's edge `10.7.20.249` with TTL 30 seconds. The running configuration was inspected; both answers were verified on 5 October 2026.

[Current-session configuration](dnsmasq.conf.template) and [team IP example](../team/team.env.example) are included in the repository. The live configuration is `/opt/homebrew/etc/dnsmasq.conf` on Aryan's Mac. Inspect before changing; keep a rollback copy.

```bash
sudo brew services list
sudo lsof -nP -iUDP:53 -iTCP:53

dig @10.7.23.16 app.team.test
dig @10.7.23.16 api.team.test
```

On Macs 2, 3 and 4, the team reports the configured DNS resolver is `10.7.23.16`. Collect `scutil --dns` plus plain `dig app.team.test` and `dig api.team.test` on at least two of those Macs. Explicit `dig @...` only proves reachability to that resolver, not the OS resolver setting.

On Aryan's own Mac the resolver is `127.0.0.1`; local DNS traffic is observed on `lo0`. Queries from another Mac reach Aryan on the LAN interface. Capture both `lo0` and `en0` when demonstrating DNS locally plus remote application traffic.

A public resolver's NXDOMAIN can be supplementary evidence for `.test`. A timeout alone does not prove namespace isolation. Do not substitute `/etc/hosts` for the team's DNS.

To restart after an intentional configuration edit:

```bash
sudo brew services restart dnsmasq
```

For problems, check the listening sockets and query the loopback and LAN address separately. Diagnose DNS before TCP, TLS and HTTP. Avoid restricting dnsmasq to `interface=lo0`, which would prevent other Macs from reaching it.
