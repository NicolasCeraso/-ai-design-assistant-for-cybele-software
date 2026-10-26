# Ports and firewall rules (optional technical layer)

Use this **only** when the task's case data says `Mostrar puertos en las conexiones: Sí` and/or
`Incluir reglas de firewall por zona: Sí`. Otherwise diagrams stay as they always were: flows
without ports. Nothing here changes the pill visual system.

**Source.** Product facts read on 2026-09-28 from the Thinfinity Architect Studio's
`docs/PORT-MATRIX.md` (Nick's "proyecto arquitectura"), which cites Thinfinity `dev-main` source
(file:line) for Thinfinity components and IANA / Microsoft Learn / RFC / vendor docs for standard
services. Knowledge only, no code from that project. **Validate with development before using a
diagram with ports or firewall rules in front of a customer.**

## The rule that decides every arrow

Only two Thinfinity components listen for connections: the **Gateway** (IN 443 HTTPS, 80 HTTP) and
the **LMServer** on the primary Broker (IN 7443 HTTPS). Brokers, RDS agents, secondary brokers and
VDI hosts have **no inbound port**: they dial **out** to the Gateway. Standard back-ends (database,
AD, FSLogix, IdP, final hosts) are servers that the broker or agent connects out to.

So an arrow always points from the side that **initiates** to the side that **listens**:
Broker → Gateway, VDI → Gateway, Broker → DB, Broker → AD, never the other way.

## Ports per component

| Component | IN (listens) | OUT (initiates) |
|---|---|---|
| Gateway | 443 HTTPS, 80 HTTP | — |
| Communication Gateway | 443 HTTPS/WSS | — (never initiates) |
| Broker, primary | 7443 HTTPS (LMServer) | 443 → Gateway · 3306 (or 1433) → DB · 389/636/88/53 → AD · 443 → IdP · 8429 → VictoriaMetrics |
| Broker, secondary | — | 443 → Gateway · 7443 → primary LMServer · native protocol → final hosts |
| Database | 3306 MySQL · 1433 SQL Server | — |
| Load Balancer | 443 HTTPS, 80 HTTP | 443 → Gateway pool |
| VDI host / RDS agent | — | 443 → Gateway · 389 → AD · 445 → FSLogix |
| FSLogix | 445 SMB | — |
| Active Directory | 53 DNS · 88 Kerberos · 389 LDAP · 636 LDAPS · 3268/3269 GC · 445 SMB · 135 RPC · 464 kpasswd · 123 NTP · 9389 ADWS · 49152–65535 RPC dynamic | — |
| IdP / SSO | 443 HTTPS | 443 (OIDC back-channel) |
| RBI cluster | 443 sessions · 6443 K8s API | 443 isolated browsing egress |
| KVM host | 443 agent · 22 SSH admin · 5900+ VM consoles | 443 reverse tunnel → Gateway |
| VictoriaMetrics | 8428 API · 8429 vmagent · 3000 Grafana · 9090 Prometheus | 443 scrape targets |
| VPN gateway | 500/UDP IKE · 4500/UDP NAT-T · 1194/UDP OpenVPN · 51820/UDP WireGuard · 443/TCP SSL-VPN | 443 → LB/Gateway |
| Final host, Windows | 3389 RDP · 5986 WinRM · 445 SMB · 5900 VNC | — |
| Final host, Linux | 22 SSH · 5900 VNC · 6000–6063 X11 · 3389 xrdp | — |
| Final host, Web | 443 HTTPS · 80 HTTP · 443 WebDAV · 443 WAG | — |
| Endpoint clients (browser) | — | 443 → Gateway/LB |

Communication Gateways: there is **no** link between the primary Gateway and a communication
gateway; the browser opens its own connection to the nearest one, and the broker registers with all
gateways. Watch-outs: WebDAV is 80/443 (not 8443); `45821–45871` are in-process values, not
firewall ports; ESP is IP protocol 50, not a port.

## Drawing ports (`Mostrar puertos en las conexiones: Sí`)

- Label format on the connector: `PROTOCOL :port`, e.g. `HTTPS :443`, `MySQL :3306`,
  `LDAP :389`. Two services on one line: `LDAP :389 · SMB :445`.
- The label is a **pill with a stroke**: white fill, 1 px `#BDBDBD` stroke, fully rounded ends
  (radius = half its height), monospace text `#373737` (Nick, 2026-09-28).
- The label sits **on** its connector, centred on a straight segment (Nick, 2026-09-28: on the line,
  not beside it). The segment must be at least the label width + 2×8 px long, plus the chevron's
  ~13 px when it ends in one, so the line shows on both sides. If it is shorter, **lengthen the
  segment** (move the pill or zone, space the rows) — do not move the label off the line, and never
  let it cover an arrowhead or a pill.
- When several connectors carry the same thing into one target (N → 1), label **one**
  representative edge, not all of them.
- Add a line to the in-SVG reference footer: `HTTPS :443` = protocol and port.

## Firewall rules per zone (`Incluir reglas de firewall por zona: Sí`)

Derive them from the drawn connectors, never invent them:

1. Every connector that **crosses a zone boundary** becomes **OUT** in the source zone and **IN**
   in the target zone, with the target's port and protocol.
2. A connector inside one zone produces no rule (e.g. Broker → DB in the same control plane).
3. Implied rules, added even without a drawn line: Broker → AD adds 389 LDAP, 636 LDAPS,
   88 Kerberos, 53 DNS; VDI → AD adds the same plus 445 SMB and 135 RPC; Broker → VictoriaMetrics
   adds 8429.
4. De-duplicate; list IN first, then by port.

Render them as a compact table per zone, inside the SVG under that zone (or as a band under the
diagram when zones are too small): a **neutral** direction chip — `IN` filled `#373737` with white
text, `OUT` outlined `#373737` on white; no green or blue, those hues belong to environment zones —
the port, then `PROTOCOL ← source` for IN or `PROTOCOL → target` for OUT.
