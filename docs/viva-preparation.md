# Viva preparation

| Prompt | What to show and explain |
| --- | --- |
| Where does DNS end? | Show the A answer and TTL. The following TCP connection is to the chosen edge. |
| How does TCP establish a session? | Point at SYN, SYN-ACK and ACK. Identify the client port, server port, sequence numbers and acknowledgments. |
| What does TLS authenticate? | Show the hostname SAN, local certificate trust, session handshake and encrypted application data. Locate the visible Certificate and ChangeCipherSpec in the TLS 1.2 trace. |
| How does nginx balance requests? | Point to the two upstreams and compare X-Edge with X-Backend across requests. |
| How does an unavailable backend recover? | Compare upstream retry logging with successful B-only responses. Explain the passive failure window and the later request that reaches A again. |
| How do DNS TTL and HTTP freshness differ? | The DNS TTL applies to name-to-address answers. Cache-Control applies to HTTP representations. An ETag lets the client validate a representation and receive 304. |
| How was isolation proved? | Show Mac 2 allowed to both ports, Mac 1 denied to both, and recovery after rule removal. Explain Mac 3's LAN hop to B and loopback hop to A. |
| What stays available when Mac 2 fails? | Mac 1 can still serve DNS. Clients with cached Mac 2 answers may fail. A healthy standby becomes useful after DNS changes and caches converge. |
| Where do cloud analogues map? | Compare private DNS with a hosted private resolver, nginx with a load balancer, and backend port policy with a security group. The actual implementation stays on the LAN. |
