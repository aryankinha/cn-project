# Phase I team demonstration script

A structured speaking guide; the supplied assignment does not specify a five-minute recording limit. Use the actual evidence and do not read pending results as completed achievements.

1. **Aryan Kinha (2401020013): topology and DNS.** Introduce four Macs and all team roles. Display architecture and inventory. Explain that app.team.test and api.team.test resolve to Divyanshu's edge. Show dig from a client configured to use Aryan's DNS, the answer IP and TTL. Show LAN and resolver evidence.
2. **Divyanshu Singh (2401010161): edge and TLS.** Display the loaded nginx configuration, both upstreams and TLS listener. Show trusted HTTPS by name without bypassing validation. Explain certificate hostname, trust, ClientHello/ServerHello and TLS termination. The edge-to-backend traffic uses HTTP.
3. **Jatin Verma (2401010200): Backend A and distribution.** Show minimal source, LAN binding and port 3001. Run repeated requests through the edge and point to both backend identifiers. Explain that nginx selects an upstream while the client knows only the edge.
4. **Jatin Kumar Singh (2401010199): Backend B and caching.** Show port 3002 and X-Backend B. Demonstrate Cache-Control, ETag and conditional 304. Distinguish a fresh cache hit from revalidation and a full response.
5. **All members: packet analysis.** Open the fresh saved capture. Identify actual DNS frame numbers, TCP SYN/SYN-ACK/ACK, socket ports and sequence/acknowledgement numbers. Show TLS handshake and encrypted records. Explain TLS 1.3 certificate visibility correctly, or demonstrate a fresh TLS 1.2 full handshake for visible Certificate/ChangeCipherSpec.
6. **All members: required failures.** Demonstrate all five Section 6.3 scenarios using the failure plan. Explain affected layers, measured outcomes and restoration. Backend failures leave DNS and the edge TLS endpoint separate from the application failure.

Finish with each member prepared to answer questions about the entire request path. Backup DNS, isolation and edge migration are Phase II topics, not claimed Phase I results.
