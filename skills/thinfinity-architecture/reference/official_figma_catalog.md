# Official Figma catalog — Cybele "Architecture Diagrams" file

> **Colores al redibujar (Nick, 2026-09-28).** Este catálogo describe lo que *hay* en Figma: zonas
> verdes por red o cliente, bus verde hacia una DB compartida, cajas violetas dentro de "Managed by
> Cybele". **Al dibujar no se copian esos colores.** Rige SKILL §2.2b:
> - verde = solo infraestructura del cliente / on-prem;
> - violeta = nube;
> - azul = hosteado por Cybele;
> - las sub-zonas de red o cliente van en gris punteado, y los buses en azul conector `#0AA9FF`.

> **Qué es:** índice + destilado del archivo oficial de Figma de Cybele con ~60 diagramas de
> arquitectura Thinfinity reales (incluye despliegues de clientes). Es la **fuente de verdad canónica**
> para topologías: cuando un prompt pide una topología nombrada o ambigua, buscá aquí la más cercana,
> **abrí esa sección en Figma para calibrar**, y recién después dibujá con las reglas de `SKILL.md`.
>
> Este doc **extiende** `thinfinity_reference_architecture.md` (capa producto). Donde aquel tiene R1–R11,
> acá están R12–R31 + vocabulario y convenciones nuevas observadas en los diagramas oficiales.
>
> **Escalera comercial (POC → Pilot → Sitio Inicial → 2 Sitios → DR):** ver **§6** al final.
>
> **Archivo:** `fileKey = W3Pnm739iwmVdo3hSaBNQe`, página `0:1` (más la página "Casos más usados", `1015:6349`, §6).
> **Cómo calibrar contra un diagrama:** `mcp__figma-remote-mcp__get_screenshot` con ese fileKey + el
> `nodeId` de la tabla §1 + `maxDimension` 1800–2800 (los diagramas son muy anchos). El metadata de la
> página completa es enorme (3 MB) — no lo cargues entero; pedí screenshots por sección.

---

## 1. Índice de secciones (node IDs)

> Muchas secciones renderizan como **board multi-variante**: V1 (notas inline) · V2 (notas al margen,
> labels abreviados) · V3 (con `Thinfinity Agent` por recurso, o con HA: LB + gateways/brokers dobles).
> El nodeId apunta a la sección entera (todas las variantes). Captura y elegí la variante más limpia.

### 1.1 Fundamentos y modelos de despliegue
| Sección | nodeId | Familia |
|---|---|---|
| Deployment options / jump-server protocol tree | `1:952`, `428:3828` | Catálogo de protocolos/targets (capability tree) |
| Single Machine Deployment (+ Local Host Connections) | `428:3828`, `426:3406` | R12 — todo en una máquina |
| Gateway on DMZ or Cloud | `123:4112` | R13 — split Gateway/Broker básico |
| Gateway on DMZ or Cloud and Secondary Broker | `428:4374`, `429:4381` | R13b — + fan-out a Secondary Brokers |
| Reverse Gateway and Primary Broker Separation | `428:3853` | R14 — separación física GW(DMZ)/Broker(LAN) |
| On Premises | `428:4157` | R15a — modelo de propiedad |
| Hybrid | `428:4159` | R15b |
| Fully Hosted | `428:4170` | R15c |
| Bring your Own Cloud (BYOD/BYOC) | `428:4167` | R15d |
| Single Tenant Cloud or Data Center | `428:4070` | R16 — server farm multi-host |
| Single Datacenter | `429:4393` | R17 — HA cross-mesh |

### 1.2 Alta disponibilidad y load balancing
| Sección | nodeId | Familia |
|---|---|---|
| Load Balancing in Primary Brokers - Local Host Connections | `428:4041` | R18 — LB sólo en brokers |
| Load Balancing Gateways Primary Brokers - Local Host Connections | `125:4654`, `429:4385` | R19 — LB en ambos tiers (mirror 2×2) |
| Load Balancing with Secondary Brokers and Multiple Gateways | `428:4152` | R20 — LB 3rd-party → N gateways → 1 PrimBroker → regiones |
| Fully Hosted - Load Balancing with agents and multiple gateways | `428:4150` | R21 — PrimBroker como spine, columnas por región |
| Load Balancing with Secondary Brokers and Multiple Gateways (alt) | `428:4152` | (ver R20) |
| Thinfinity Failover Architecture | `428:4155` | R22 — duplicación de sitio completo (Primary/Backup) |

### 1.3 Multi-tenant / multi-network / apps+DB
| Sección | nodeId | Familia |
|---|---|---|
| Multiple Networks | `428:4061` | R23 — por-red Firewall + Secondary Broker |
| Multiple VDI Pools | `428:4057` | R6 (ya existe) — pools como sub-zonas |
| Multi-Domain Multi-Tenant Hybrid Deployment | `428:4098` | R24 — multi-IDP + multi-plataforma, 1 broker |
| Multi-Tenant Deployment | `428:4106` | R25a — tenant por plataforma, broker por tenant |
| Multiple-Tenant Deployment | `429:4391` | R25b — tenant por cliente (Resource Group/apps/URL/SAML) |
| Multiple Applications Single Database | `428:4110` | R26 — zonas-sitio → DB compartida (bus verde) |
| Multiple Application Servers Single Database | `428:4117` | R27 — N×(App Server + Sec.Broker) → 1 SQL |

### 1.4 Seguridad / acceso / OT / IDP
| Sección | nodeId | Familia |
|---|---|---|
| ZTNA Diagram (resource/connector tree) | `426:3403` | Catálogo de targets por conector |
| Role-Based Access Control (RBAC) | `426:3404` | R28 — pipeline de roles/permisos |
| Behind Palo Alto Networks | `428:4085`, `428:4087` | R29 — NGFW 3rd-party inline |
| Connect IT and OT Networks | `428:4092` | R30 — bridge IT↔OT |
| OT and Offline | `428:4077` | R31 — datacenter autónomo / offline |
| WAG (Web Application Gateway) | `428:4145` | R32 — fan-out a web backends |
| Detailed Integration Auth0 | `428:4120` | Plantilla IDP detallada (handshake) |
| Detailed Integration Entra ID | `428:4123`, `428:4129` | Plantilla IDP detallada (provider-agnostic) |

### 1.5 Enterprise VDI on OCI + clientes reales
| Sección | nodeId | Notas |
|---|---|---|
| Enterprise VDI on OCI - Inside Network Perimeter (global/GeoIP) | `428:4136` | Comm Gateways por región + Primary/Secondary broker |
| Enterprise VDI on OCI (single-region estándar) | `430:4396`, `428:4139`, `430:4401`, `430:4406`, `430:4411`, `430:4417`, `430:4425` | TLS-443 in / No-Inbound-Port; Oracle Cloud zone |
| Entel Chile | `431:4500` | HA + FSLogix + dual MySQL (escalado en 3 tiers) |
| Claro | `430:4423` | OCI estándar re-skinned "Claro Datacenter" |
| Rimac | `431:4495` | DR dual-site + gateways Internal/External (1000 users) |
| Banco Estado | `431:4496` | Dual-site Oracle + replicación MySQL cross-site |
| Oracle Peru | `464:3673` | HA pair + App Pool/Subnet + Linux/Ubuntu |
| Telefonica Brasil | `450:3536`, `431:4928` | 11 gateways fan-out bajo 1 LB |
| SUNARP / Distecna / Telefónica Colombia / Oracle Peru / Rede Americas | `431:4497` `431:4499` `442:3617` `446:3504` `446:3813` `464:3673` `453:3536` `453:3821` | Variantes cliente del patrón HA estándar |
| Sandbox para TW best practices | `486:3985` | Board grande de trabajo (6145×7087) |

---

## 2. Vocabulario nuevo (extiende `thinfinity_reference_architecture.md` §1–§2)

### 2.1 Componentes / pills nuevos (icono sugerido del set de 132)
| Pill (label literal) | Icono | Rol / notas |
|---|---|---|
| `Thinfinity Agent` | `thinfinity` | **Componente propio**, distinto del Gateway. Se instala en cada recurso/VM y marca saliente al Broker. En diagramas de cliente aparece **una pill Agent junto a CADA recurso**. |
| `Thinfinity Reverse Gateway` | `gateway` | Nombre completo del Gateway en diagramas de integración IDP detallada. |
| `Virtualization Process` | `app-virtualization` | Parte del stack de software de un host (orden: Agent → Gateway/Broker → Virtualization Process → Desktop/Remote Apps). |
| `Desktop / Remote Apps` | `remote-app` / `desktop` | Recurso co-alojado en el host del Broker. |
| `Thinfinity Gateway + Prim Lic. Manager` | `gateway` | Gateway con License Manager embebido; se duplica por sitio en Failover (R22). |
| `Load Balancer` / `Load Balancer / WAF` | `load-balancer` | LB genérico (front de gateways). La variante `/ WAF` agrega WAF. |
| `Load Balancing` | `load-balancer` / `internal-session-brokering` | Nodo LB genérico **entre** gateway y brokers (R18/R19). |
| `Nginx/ Reverse Proxy/ App Gateway/ AWS Load Balancer/ Palo Alto Server` | `proxy` | Pill multilínea = LB de terceros nombrado explícitamente (R20/R22, R27 V3). |
| `WAF` | `shield` / `layered-security` | Web Application Firewall (perímetro). En clientes suele dibujarse como **línea vertical dashed** etiquetada, no pill. |
| `WAG` | `web-app` / `proxy` | Web Application Gateway: nodo reverse-proxy que abre a backends web (R32). |
| `Palo Alto` | `firewall` / `shield` | NGFW de terceros, inline en el ingress (R29). Sin icono dedicado → usar `firewall`. |
| `OAuth Token` / `OAuth / SAML Token` | `saml` / `key` / `secure-password` | **Token como pill discreta** en el handshake IDP (provider → token → broker). |
| `SAML Token`, `SSO / 2FA` | `saml`, `2FA` | Etapas de auth en el ingress. |
| `Unique Remote ID` | `id` / `authenticated-cloud` | Tarjeta por-VM: cada VM es individualmente direccionable (R20/R21). |
| `Protocol Encapsulated Over SSL (TLS 1.3 Encryption)` | `lock-check` / `vpn-tunnels` | Pill candado en el cable que marca el encapsulado. |
| `TLS 1.3 Traffic Port 443` | `vpn-tunnels` | **Pill de cable de ingreso** (entrada pública). |
| `TLS 1.3 Traffic No Inbound Port` | `vpn-tunnels` | **Pill de cable de retorno** Gateway↔Broker (conexión inversa). Sinónimos: `Only Outbound Connections`, `Firewall No Inbound Port(s)`, `TLS 1.3 Outbound Traffic`. |
| `Firewall Port 443` | `firewall` | Variante simple del firewall de ingreso. |
| `MySQL Data Base` / `SQL Data Base` / `SQL` / `SQL Database / File Server` | `database` / `databases` | **Config DB** (estado/licencias). HA = doble MySQL o flecha de replicación cross-site. |
| `FSLogix` + `User Profile` (en sub-zona `Storage`) | `fslogix` / `profile` | Almacén SMB de perfiles para pools VDI. |
| `Virtual Machine` | `vm` | Host que corre el Gateway (DMZ). |
| `Engineering Workstation` | `workload` / `gpu-fast` / `pc` | Estación OT/CAD. |
| `PLC` / `SCADA / PLC` | `manufacture` / `monitor-VM` / `system-config` | Controladores OT. |
| `Pump` / `Motor` | `manufacture` (fallback) | Actuadores físicos OT (sin icono dedicado). |
| `Linux Server` (`Ubuntu`) | `linux` | Pool Linux (cliente real Oracle Peru). |
| `Windows Server VDA` / `Windows 11 VDI` / `Windows 10 VDI` / `Windows Server VDI` | `windows` / `vdi` | Nombres de recurso usados por clientes reales. |
| `Virtual Applications` / `Virtual Application Pool` | `app-virtualization` / `app-group` | Apps publicadas. |
| `Session Based Servers` / `Application Servers` / `Physical Workstations` / `1 to 1` | `server` / `app-server` / `pc` / `user-vm` | Taxonomía de recurso del reference single-tenant (R16). `1 to 1` = VDI 1-a-1. |
| `App Pool` / `Application Pool` (sub-zona dentro de `Subnet`) | `app-group` | Agrupación de recursos en clientes OCI. |
| WAG backends: `IIS Server`→`Dynamics`, `Apache`→`Wordpress`, `Node.js`→`ERP` | `windows`/`web`/`web-app` | Pareo web-server → app (R32). |

### 2.2 Catálogo de IDPs (RBAC `426:3404`)
Cluster de pills bajo zona `External IDP` / `IAM`, federados vía pills `SAML` + `OAuth 2.0`:
`Google` `Microsoft AD` `Microsoft Entra ID` `Okta` `DUO` `ForgeRock` `Auth0` `OCI IAM` `Jumpcloud`
`PingID` `Onelogin`. Iconos: `google entra-id active-directory duo forgerock auth0 oracle` + genérico
`id`/`saml` para Okta/Jumpcloud/PingID/Onelogin (sin icono dedicado).

### 2.3 Catálogo conector → target (ZTNA tree `426:3403` + jump-server tree)
Conectores (pills azules): `RDP` `VNC - RFB` `SSH - VT` `WAG` `WebDAV` `VirtualUI` `ThinVNC`
`TN5250 - TN3270`. Intermedios: `Windows App` `Desktop` `SSH / Telnet` `Web Folders` `Shared Desktops`
`Systems` `Web App` `Network Drivers / NAT` `Telnet - AS400`. Hojas (targets, pills negras):
`Virtual Application` `Virtual App Pool` `VDI / Cloud VDI` `Terminal Server` `Desktop Computer`
`Routers / Switch` `Console Based Applications` `Admins Panels` `Intranet (CRM/ERP/ACCTG/SCADA)`
`IoT Controllers` `Camera CCTV Controllers` `X-Windows` `Shared Desktop` `Linux` `macOS`
`IBM z series` `IBM i series` `Unix`. Útil como **librería de targets** para prompts tipo "a qué puede
acceder Thinfinity".

### 2.4 Zonas y etiquetas de propiedad nuevas
| Zona / label | Significado |
|---|---|
| `Local Host` / "All Components in ONE MACHINE" | Todos los componentes en un solo host (R12). |
| `Machine` / `Virtual Machine` (host container) | Caja-host con motif lupa (§3.1). |
| `Managed by Cybele` / `Managed by Customer` / `Managed by you` / `Your Cloud – Managed by Cybele` | **Etiquetas de propiedad** que codifican el modelo de despliegue (R15). |
| `Thinfinity Portal` | Zona que envuelve al Gateway (sinónimo de la zona DMZ/Cloud del gateway). |
| `DMZ or Cloud` | Sub-label de ubicación flexible del Gateway. |
| Region zones: `USA` `Asia` `Europe` `Tokyo` `New York` | Bandas geográficas (map-pin). |
| Site zones: `Primary Site` / `Backup Site`, `Site 1` / `Site 2` | DR / failover. |
| `Corporate Domain` → `Secondary Domains` | Dominios anidados (RBAC). |
| `App Pool` / `Application Pool` dentro de `Subnet` | Recursos OCI. |
| `Customer Network`, `IT Domain`, `OT Network` | Zonas de red por tier. |
| `Resource Group N / n Users` | Sub-zona verde por tenant/cliente (R25b). |
| `Oracle Cloud (OCI)` / `Claro Datacenter` (cualquier nombre de cliente) | **El borde de nube se renombra por cliente** — conserva el vocabulario interno, rebrandea el perímetro. |

---

## 3. Convenciones visuales nuevas (extiende `SKILL.md`)

> Estas son **observadas en los diagramas oficiales**. Algunas son ricas (motif lupa, captions de
> propiedad) y se usan en diagramas conceptuales/comerciales; los diagramas de cliente reales son más
> austeros (monocromo azul, perímetros como líneas dashed). Elegir el registro según el pedido.

1. **Motif "lupa" (host + burbuja).** Un host se dibuja como ícono de torre/servidor y una **burbuja de
   aumento** que revela el stack de software adentro (orden canónico: `Thinfinity Agent` → `Gateway`/
   `Primary Broker`/`Secondary Broker` → `Virtualization Process` → `Desktop / Remote Apps`). El host del
   **Gateway** lleva sólo Agent+Gateway; el host del **Broker** lleva Agent+Broker+Virtualization+Desktop/
   RemoteApps. Útil para diagramas "cómo funciona". En diagramas austeros, cada uno es una pill normal.
2. **Escala-out `⋮` / `•••`.** Dos filas idénticas + una elipsis vertical (`⋮`) o horizontal (`•••`)
   = "repetir N / N más". Es la forma canónica de mostrar pools/VMs/brokers múltiples sin dibujarlos todos.
3. **Conexión inversa redundante.** Además de la flecha apuntando al Gateway (I1), los diagramas la marcan
   con **captions**: `No Inbound Port(s)`, `Only Outbound Connections`, `TLS 1.3 Traffic No Inbound Port`,
   `TLS 1.3 Outbound Traffic`. La entrada pública se marca `TLS 1.3 Traffic Port 443` / `Firewall Port 443`.
   En clientes el retorno suele ser un **bus azul en bucle** por arriba y abajo del clúster gateway/broker.
4. **Modelo de despliegue por 2 ejes ortogonales** (R15): etiqueta de **propiedad** (`Managed by Cybele`
   vs `Managed by Customer`) × **ubicación por color/icono** (verde+edificio = on-prem/cliente;
   morado/azul+nube = cloud). On-Prem = broker on-prem del cliente; Hybrid = uno on-prem (verde) + uno
   cloud Cybele (morado); Fully Hosted = todo dentro de una caja `Managed by Cybele Software`, brokers
   cloud; BYOD/BYOC = Gateway Cybele + brokers en la **nube propia del cliente** (Managed by Customer +
   icono nube).
5. **Perímetro como líneas, no cajas (estilo cliente real).** Clientes dibujan `WAF` y `Firewall` como
   **líneas verticales dashed etiquetadas** y un `Subnet`/`App Pool` dashed, en vez de zonas-caja. El
   reference idealizado usa cajas (DMZ, Network 1/2/3). Ambos válidos; seguir el registro del pedido.
6. **Board multi-variante.** Un mismo diagrama suele venir como V1 (notas inline) / V2 (notas al margen,
   labels abreviados `App Server`/`Sec. Broker`) / V3 (con `Thinfinity Agent` por recurso, o con HA: LB +
   gateways/brokers dobles). Al generar, elegir UNA variante salvo que el usuario pida comparar.
7. **Bloques de texto-beneficio.** Algunos diagramas comerciales (WAG, OCI global) llevan paneles de texto
   al costado: "Secure Remote Access / No Client Installation / Enhanced Usability / Streamlined IT Admin",
   "Global Deployment Readiness / GeoIP Functionality". Convención de documentación, opcional.
8. **Bus colector verde para DB compartida** (R26): cuando N zonas comparten una sola DB, un bus
   colector (a veces verde) las une a UNA pill `SQL Database / File Server`. (Excepción puntual al
   monocromo; el resto del diagrama queda azul.)
9. **Dos registros de endpoint.** Diagramas de despliegue detallado: `Browser Access` / `Thin Client` /
   `PWA` / `Client Access` / `Windows Client` / `Android Tablets`. Diagramas de capacidad/legend:
   `User Group 1/2/n` bajo `Remote Access` + `Local Users`.
10. **Diagramas de cliente = monocromo azul.** Ningún despliegue real usa color-coding por protocolo
    (R9). El color-coding queda como feature del reference idealizado y opt-in (SKILL §8).

---

## 4. Recetas nuevas R12–R32 (todas 🟢 — respaldadas por el Figma oficial)

> Sumar a la tabla §6 de `thinfinity_reference_architecture.md`. La columna "Fuente" es el nodeId §1.

| Receta | Patrón | Cuándo usarla | Fuente |
|---|---|---|---|
| **R12 — Single Machine** | Users → Firewall 443 → 1 host con Gateway+Primary Broker+Virtualization+Desktop/RemoteApps. Sin DMZ ni split. Tagline "sin exponer 3389/80". | demo / instalación mínima de un solo servidor | `426:3406`, `428:3828` |
| **R13 — Gateway DMZ/Cloud + Broker** | Users → FW443 → Gateway(DMZ, Agent+Gateway) ← FW No-Inbound ← Broker(Agent+Broker+Virt+Desktop). | despliegue estándar de 2 hosts | `123:4112` |
| **R13b — + Secondary Broker fan-out** | R13 + Primary Broker abre a N `Secondary Broker`+`Virtualization` (con `⋮`). | escalar recursos detrás de un broker | `428:4374` |
| **R14 — GW/Broker Separation** | Gateway aislado en DMZ entre **dos firewalls**; Primary Broker en LAN privada marca saliente ("No Inbound Port"). + árbol de protocolos. | enfatizar el modelo de seguridad / aislamiento del gateway | `428:3853` |
| **R15 — Modelos de propiedad** | a) On-Prem · b) Hybrid · c) Fully Hosted · d) BYOD. Eje propiedad×ubicación (§3.4). | "¿on-prem / híbrido / SaaS / nube propia?" | `428:4157/4159/4170/4167` |
| **R16 — Single-Tenant server farm** | 1 Gateway + 1 Primary Broker → `Server 1..N`, cada host con `Thinfinity Agent` + tipo de recurso (`Session Based`/`1 to 1`/`Physical Workstations`/`Application Servers`). Legend On-prem/Cloud/Hypervisor. Cables `TLS 1.3 443` / `No Inbound Port`. | un tenant, granja multi-host | `428:4070` |
| **R17 — Single Datacenter HA** | Users → WAF → Firewall → Load Balancer → **2×Gateway** (cross-mesh) **2×Broker** → SQL compartida → recursos; bus de retorno arriba+abajo. | HA redundante en un datacenter | `429:4393` |
| **R18 — LB en Primary Brokers** | 1 máquina Gateway → nodo `Load Balancing` → **N Primary Broker hosts** (broker co-alojado con recursos = "Local Host Connections"). LB sólo en tier broker. | escalar brokers, gateway único | `428:4041` |
| **R19 — LB Gateways + Brokers** | `Load Balancer / WAF` → **2 Gateway hosts**; spine central `Load Balancing — Firewall No Inbound — Load Balancing`; → **2 Broker hosts**. Mirror 2×2, ambos tiers balanceados. | HA/escala en ambos tiers | `125:4654` |
| **R20 — Multi-Gateway + Secondary Brokers** | Customers → LB 3rd-party (Nginx/AWS/Palo Alto) → **N gateways como dominios web** (`www.1/2/3.com`) → **1 Primary Broker central** → region zones (USA/Asia/Europe) con VMs `Unique Remote ID` + `Thinfinity Agent` (= secondary/edge brokers). Hub-and-spoke. | SaaS multi-gateway global | `428:4152` |
| **R21 — Fully Hosted multi-región** | `Primary Broker` como **spine superior** que fan-out a columnas autónomas por región (cada una con sus users + gateway `www.N.com` + VMs/agents). | SaaS fully-hosted multi-región | `428:4150` |
| **R22 — Failover (DR)** | LB front → **dos lanes paralelos** `Primary Site` y `Backup Site`, cada uno completo: `Gateway + Prim Lic. Manager` ← `Thinfinity Prim. Broker` ← sitio con N `Secondary Broker` (`•••`) + App/VDI. HA por **duplicación de sitio entero**. | failover / disaster recovery | `428:4155` |
| **R23 — Multiple Networks** | 1 Gateway + Broker central (con `Corporate Domain` + IDPs externos) → **N zonas-red verdes**, cada una self-contained con su `Firewall` + `Secondary Broker` + filas recurso+Agent. Caption "No Inbound Port Required". | varias redes aisladas tras un gateway | `428:4061` |
| **R24 — Multi-Domain Multi-Tenant Hybrid** | Multi-IDP por dominio (Azure AD/Okta en zonas user) + **1 Gateway + 1 Primary Broker** → múltiples **plataformas** (On Premises/Azure/Nutanix) como zonas color. | híbrido con varios IDPs y plataformas, broker compartido | `428:4098` |
| **R25a — Multi-Tenant por plataforma** | 1 Cloud Gateway (Managed by Cybele) → **1 Primary Broker por tenant**, tenant = zona por hosting (Azure/Datacenter/Private Cloud), caption `User Group X / N Users`. | SaaS multi-tenant por entorno | `428:4106` |
| **R25b — Multi-Tenant por cliente** | Igual pero tenant = **Customer N**, recursos = apps publicadas (`Server ERP`, `App Web`, `URL`, `SAML`) en sub-zona verde `Resource Group / n Users`. | SaaS multi-tenant por cliente | `429:4391` |
| **R26 — Multiple Apps, Single DB** | Zonas por sitio (ciudades) → **bus colector (verde) → UNA pill `SQL Database / File Server`**. | varios entornos comparten una DB | `428:4110` |
| **R27 — Multiple App Servers, Single DB** | `Customer Network` con N×(`Application Server` + `Secondary Broker` dedicado) bajo 1 Primary Broker, todos → 1 pill `SQL`. V3: + LB/reverse-proxy + dual GW + dual Primary Broker. | granja de app servers con DB única | `428:4117` |
| **R28 — RBAC** | Catálogo IDP (`External IDP`/`IAM`) → `SAML`+`OAuth 2.0` → zona verde `Users assigned to roles` → nodo `Admin assigns users to appropriate roles` → `Roles define authority level` → `Permissions authorized for specific roles` → recursos. Dentro de `Corporate Domain`→`Secondary Domains`. | explicar control de acceso por roles | `426:3404` |
| **R29 — Behind Palo Alto (3rd-party NGFW)** | NGFW (`Palo Alto`) **inline** users→NGFW→`SSO/2FA`→`TLS 1.3`→Gateway; Thinfinity queda **detrás** reverse-only. Glifo "pin/gota" Gateway(arriba)+Primary Broker(abajo). | desplegar detrás de un firewall existente | `428:4085` |
| **R30 — Connect IT and OT** | `IT Users`+`OT Users` → 1 Gateway (DMZ); Primary Broker (IT Domain) saliente al gateway; zona `IT` (Sec.Broker+Machines) + zona `OT Network` con cascada `Engineering Workstation/Server → PLC / SCADA → Pump / Motor`. IT y OT comparten gateway, brokers separados. | unir redes IT y OT | `428:4092` |
| **R31 — OT and Offline** | Todo dentro de UNA zona `Datacenter`, sin IDP externo; `TLS 1.3 443` in / `No Inbound Port` out; **`Thinfinity Agent` por recurso**; recursos segmentados en `Network 1/2/3`. Variante offline: sin gateway cloud. | despliegue autónomo / aislado / sin nube | `428:4077` |
| **R32 — WAG (web app gateway)** | Users → Firewall → Encryption → Gateway(DMZ) → Broker → `WAG` → fan-out a web servers (`IIS`/`Apache`/`Node.js`) → apps (`Dynamics`/`Wordpress`/`ERP`), backends en zona `No Inbound Port Required`. | publicar apps web clientless | `428:4145` |
| **R33 — Zero Inbound Ports / ZTNA clean (OCI)** 🟢 | Remote Access (`Browser Access`/`Thin Client`/`PWA`) → `TLS 1.3 Port 443` → `Thinfinity Gateway` (zona "Edge · No Listener"); zona `Identity` (`Identity · MFA / Per-app authz`) → **flecha punteada de auth** al Gateway; del lado privado, zona `OCI Tenancy · Private Subnets` con `VDI Session Hosts` + `Application Servers`, cada uno con su `Thinfinity Agent` → `Thinfinity Broker` → pill `Outbound-only TLS / No Inbound Port` → Gateway. **Todas las flechas del lado privado apuntan al Gateway** (saliente; cero entrantes al subnet). | "zero inbound ports / remove the inbound listener / sin VPN portal / reemplazo de SSL-VPN / ZTNA sobre cloud (OCI)" | artefacto `zero_inbound_ztna_oci.html` (variante limpia de R13 + énfasis ZTNA; deriva de OCI VDI `430:4396`) |

### 4.1 Plantilla "Detailed IDP Integration" (provider-agnostic)
Fuente: `428:4120` (Auth0), `428:4123` (Entra ID). Reusar tal cual, parametrizando el provider:

- Columnas/swimlanes L→R: `Remote Access`(users) → `Only Outbound Connections`(TLS 1.3 + Firewall) →
  `DMZ`(`Thinfinity Reverse Gateway`) → `Only Outbound Connections` → `Customer Domain`(Location A
  "conexión local, sin puertos" + Location B "No Inbound Ports" con Application Pool de Secondary Brokers).
- **Handshake auth** dibujado como sub-flujo vertical: `<Provider pill>` → `<Token pill>` →
  `Thinfinity Primary Broker`. Provider = `Auth0` / `Microsoft Entra ID` / etc.; Token = `OAuth Token`
  (Auth0) o `OAuth / SAML Token` (Entra). El broker lleva footnote: `*SAML Authentication. *Role Based
  Permission Enforcement. *User Mapping.`
- Broker → flecha **hacia arriba/saliente** al Reverse Gateway (inversa). Entra además **taggea cada fila
  de usuario** con el glifo del provider.

### 4.2 Enterprise VDI on OCI — dos sabores
- **Single-region estándar** (`430:4396`, Claro `430:4423`): 1 Gateway (DMZ) + 1 Broker; cables explícitos
  `TLS 1.3 Traffic Port 443` / `TLS 1.3 Traffic No Inbound Port`; zona externa branded (`Oracle Cloud
  (OCI)` / `Claro Datacenter`); recursos en `Network 1/2/3`; variante con `Thinfinity Agent` por recurso.
- **Global / GeoIP** (`428:4136`): `Communication Gateway` nombrados por región/ruteo + jerarquía
  `Primary Broker` (hub central) + `Secondary Broker` (por región Europe/USA/Tokyo). Paneles
  "Global Deployment Readiness" + "GeoIP Functionality".

### 4.3 Patrones de clientes reales (que el reference idealizado omite)
- **DR dual-site** (Rimac `431:4495`, Banco Estado `431:4496`): `Site 1`/`Site 2` espejados; Banco dibuja
  **flecha de replicación MySQL cross-site**.
- **Gateways Internal/External** (Rimac): split-horizon — `Thinfinity Gateway (External)` +
  `(Internal)` por audiencia, no por HA.
- **Fan-out masivo de gateways** (Telefonica Brasil `450:3536`): **11 gateways** bajo 1 LB con sólo 2
  brokers → gateways escalan independiente de brokers.
- **FSLogix Storage subnet** (Entel `431:4500`): `FSLogix` + `User Profile` en sub-zona `Storage`,
  flecha teal desde recursos; + **doble MySQL** (Config DB redundante).
- **Diagrama de 3 tiers de madurez** (Entel): single-node → HA+dual-DB → +FSLogix, apilados como historia
  de escalado en un solo frame.
- **Pools Linux/Ubuntu** (Oracle Peru `464:3673`): `Linux Server`(`Ubuntu`) como recurso de primera clase;
  `App Pool`/`Application Pool` dentro de `Subnet`.

---

## 5. Gaps de iconos detectados
Sin icono dedicado en el set actual (usar fallback indicado): **Pump/Motor** (`manufacture`),
**WAF** (`shield`), **Palo Alto** (`firewall`), **Nginx** (`proxy`), **Okta/Jumpcloud/PingID/Onelogin**
(`id`/`saml`), **Dynamics/Wordpress/ERP** (`web-app`), **Android Tablets** (`notebook`/`multi-platform`).
Si Nick quiere fidelidad de marca en estos, conviene agregarlos al set `icons/`.

---

## 6. Casos más usados — la escalera comercial (Figma, página "Casos más usados", 2026-10-27)

> **Fuente:** misma `fileKey W3Pnm739iwmVdo3hSaBNQe`, página `1015:6349` ("Casos más usados"). Es el
> archivo ordenado con los diagramas que la empresa usa en conversaciones de ventas. Su columna
> izquierda (~50 secciones "Architecture sample…") repite las de §1 con IDs `1015:*`; los IDs `428:*`
> de §1 **siguen siendo válidos**. Lo nuevo son las dos columnas de la derecha, que este §6 indexa.
> Los node IDs de abajo llevan el prefijo `1015:` implícito.
>
> **Decisiones de Nick (2026-10-27):**
> - **Registro visual:** se dibuja con el sistema de **pills** de SKILL.md. De estos diagramas se toma la
>   **topología** (qué componentes van y dónde), no el estilo: las cajas-host "Windows Server" con el
>   componente adentro y la Subnet lavanda del Figma **no** se copian.
> - **Colores de entorno:** rige SKILL §2.2b. El OCI en rojo punteado y Azure en verde azulado del Figma
>   **no** se copian (nube = violeta, on-prem = verde, Cybele = azul).
> - **Tramos de usuarios orientativos:** "50–1000" y "100–1000" son el mismo caso (el gráfico nació de
>   un uso real y quedó en el repositorio); 999 o 1000 es lo mismo. No usar el número como corte duro.

### 6.1 La escalera (elegir UN escalón; cada uno suma al anterior)

| Escalón | Qué dibuja | Cuándo | Nodos (Windows Server / Windows 11 · Linux) |
|---|---|---|---|
| **E1 — Prueba de Concepto** | Users (Windows Client + Browser Access) → **1 Gateway** ← **1 Broker**; Subnet con N agentes (`⋮`/`•••`). Sin LB, sin DB, sin firewall. Bus de retorno arriba y abajo. | POC, demo, evaluación | Gateway Windows: `7457` (pool Windows Server) · `7723` (pool Windows 11) · Gateway Linux: `7590` (Windows Server) · `7832` (Windows 11) |
| **E2 — Pilot to Production** | E1 + **Load Balancer** tras línea `Firewall`. Recursos mezclan Windows 11 y Windows Server. | piloto que pasa a producción | `7941` · `8045` · con App Pool: `8842` · `8951` |
| **E3 — Sitio Inicial (50–1000 usuarios)** | Users → `WAF` · `Firewall` → LB → **2 Gateways** ⇄ **2 Brokers** (cruzados) → **Profiles (MySQL Database)** + **Analytics (MySQL HeatWave)**; **Monitoring Server** con línea punteada al Broker; Subnet con agentes. | sitio de producción único, con HA | Win 11 `7093` · Linux `7275` · `46317` |
| **E3b — Sitio Inicial + Application Pool** | E3 con varias **Subnets** (A/B/C), cada una con su **App Pool** (Windows Server · Windows 11 · Linux/Ubuntu). | recursos en varias redes o de varios SO | GW Windows + pool Windows `8149` · GW Windows + pool Linux/Ubuntu `11030` · GW Linux + pool Windows `8373` · GW Linux + pool Linux/Ubuntu `11266` · pool mixto `8597` · `46072` |
| **E3c — Sitio Inicial + sitio secundario (activo-pasivo)** | **Site 1** = E3 completo. **Site 2 reducido**: `Load Balancer` **sin flecha de usuarios** → 1 Gateway ← 1 Broker ← 1 `MySQL Database`, + Monitoring Server y su Subnet. El Broker del Site 2 abre **además hacia los 2 Gateways del Site 1** (dos flechas largas que cruzan la línea Firewall). Réplica bidireccional entre las bases. Ver §6.5. | dos ubicaciones: una principal y otra secundaria / de respaldo | `10332` · Linux `10681` |
| **E4 — 2 Sitios Activo-Activo (1000 a 5000)** | **Site 1 y Site 2 simétricos**: cada uno con sus Users, WAF · Firewall, LB, 2 GW ⇄ 2 Brokers, base(s) y Subnet. **Sin flechas Broker→Gateway entre sitios.** Réplica bidireccional vertical entre las bases. Tres niveles de detalle: **rico** (Profiles + Analytics + Monitoring; Subnet con Windows Server + Windows 11) `9484` · Linux `9908`; **medio** (1 `MySQL Data Base` por sitio) `13073` (ES); **simple** (1 `SQL Data Base`, pool `Windows Server VDI`) `12327` (EN). Ver §6.5. | gran escala, dos sitios activos | ver columna Qué dibuja |
| **E5 — Sitio Inicial con Disaster Recovery** | Sitio principal (Users, WAF · Firewall, LB, 2 GW ⇄ 2 Brokers, 1 SQL, pool de recursos) + **sitio de recuperación** debajo: `URL Recovery` → 1 GW ← 1 Broker → 1 SQL + su pool. El Broker de recuperación abre hacia **los 2 Gateways del principal**. Réplica SQL ↔ SQL bidireccional. Separados por línea punteada. Ver §6.5. | recuperación ante desastres | EN `12614` (pool: Windows Server VDI · Windows 10 VDI · Virtual Applications) · ES `12811` (Subnet Windows 11 + Windows Server) |

### 6.2 Modelos básicos y casos de cliente

| Caso | Qué muestra | Nodo |
|---|---|---|
| **Basic Architecture** | User 1…n → Gateway ← Broker; Subnet de Windows Server o Windows 11, con `⋮`. Sin LB ni DB. | `11735` (Server) · `11829` (Win 11) |
| **Basic model** | 4 Users → Firewall → LB → 1 Gateway ← 1 Broker; pool de `Thinfinity VDI`. | `15471` |
| **Basic model Prod – Claro Chile** | 3 Users → LB → **3 Gateways** ← **2 Brokers** ← 1 MySQL; Subnet Windows 11. Referencia de fan-out de gateways. | `15690` (POC: `15613`) |
| **Basic model POC (Claro Chile)** | 1 User → Firewall → LB → 1 GW ← 1 Broker; Subnet con 4 `Windows Server`. El POC de Claro ya lleva LB y firewall (a diferencia de E1). | `15613` |
| **OCI + Azure — mínimo** | Users (Windows Client + Browser Access) → WAF · Firewall → **1 GW ← 1 Broker dentro de OCI**; la Subnet de 6 `Windows Server` + Agent en **Azure**. Sin LB ni base. Versión simple de `45395`. | `45754` |
| **Initial Site + FSLogix** | 2 GW ⇄ 2 Brokers + MySQL; zona **Backend Apps** (Windows Server) con flecha bidireccional a una zona **Storage** (FSLogix + User Profile). | `13987` |
| **Initial Site – VDI pool** | 2 GW ⇄ 2 Brokers + SQL; pool mixto en caja gris: `Windows Server VDI`, `Windows 10 VDI`, `Virtual Applications` (sin Subnet). | `13393` |
| **Initial Site – 4 Gateways + GPU** | LB → **4 Gateways** (fan-out); 2 Brokers unidos por un bus que alimenta a los 4; 1 SQL; pool `Windows 10/11 VDI` + `Windows GPU Instance`. | `14171` |
| **Basic model + FSLogix** | Users → LB → 1 GW ← 1 Broker; Subnet con 6 Windows Server y zona **Storage** (FSLogix + User Profile) con flecha bidireccional (verde en el Figma → azul conector acá, §2.2b). | `15257` |
| **Pilot to Production – App Pool (dos datacenters)** | **Oracle Datacenter (Bogotá)**: LB → GW ← Broker; pill `FastConnect VPN` (flecha bidireccional) hacia **Kyndryl Datacenter (Bogotá)** con App Pool de Windows Server + Agent. Cliente real; el enlace es VPN, no la conexión inversa estándar. | `8842` (Gateway Windows) · `8951` (Gateway Linux, Users con Linux Client) |
| **Perú + Chile** | Dos orígenes de usuarios (Perú, Chile) → un LB → **grupos de GW + Brokers por país**, cada uno con su Subnet etiquetada `País – N Usuarios`; 2 MySQL. | `39827` |
| **OCI + Azure Infrastructure** | Control plane (LB, 2 GW, 2 Brokers, MySQL) en una nube; la Subnet de agentes en **otra** nube. Mismo patrón que R24, simple. | `45395` · `45754` |
| **Thinfinity + OCI + Monitoring (Linux)** | E3 dentro de un entorno OCI, con Monitoring Server. | `45558` |
| **Tu Recobro – Colombia (OCI + Linux)** | Windows Client → LB → 2 GW ⇄ 2 Brokers + 1 MySQL; Subnet con 6 `Linux Server VDI`, cada uno con un pill `Ubuntu` (en lugar del Agent). | `39669` |
| **Multi-tenant** (comercial) | Estilo "Thinfinity Hosted": Gateway + Prim. Broker en zona cloud, Customer Hosted con pools secundarios; flechas de tres colores por flujo. | `44762` |

### 6.3 Vocabulario nuevo (traducido a pills)

| Elemento del Figma | Cómo se dibuja acá | Icono |
|---|---|---|
| `Monitoring Server` | pill secundaria; **línea punteada** `#0AA9FF` de telemetría hacia el Broker (no es flujo de usuario) | `broker-monitor` / `monitor-VM` (verificar; el Figma usa un ojo) |
| `Profiles` + `MySQL Database` | zona gris punteada `Profiles` con una pill `MySQL Database` | `database` |
| `Analytics` + `MySQL HeatWave` | zona gris punteada `Analytics` con una pill `MySQL HeatWave` | `database` (sin icono dedicado: gap) |
| `URL Recovery` | pill secundaria a la izquierda del Gateway del sitio de recuperación | `refresh` |
| `WAF` y `Firewall` | **líneas verticales punteadas con etiqueta**, no pills (como §3 punto 5) | — |
| `Subnet` / `App Pool` | zona gris punteada con etiqueta; dentro del Subnet, un App Pool por red | `network` / `app-group` |
| Recurso = **host + Agent** | una pill de recurso con su etiqueta de SO (`Windows 11`, `Windows Server`, `Linux Server · Ubuntu`) y el `Thinfinity Agent`; `⋮`/`•••` para repetir | `windows` · `linux` · `thinfinity` |
| Variantes **"Linux"** del título | **El título no dice qué es Linux: hay combinaciones independientes.** Eje Gateway: `Windows Server` o `Linux Server`; si es Linux, Users lleva `Linux Client` en vez de `Windows Client`. Eje recursos: `Windows 11`, `Windows Server` o `Linux Server` + `Ubuntu`. **Brokers: `Windows Server` en todos los frames vistos.** Ejemplos: GW Windows + pool Linux `11030`, `39669`; GW Linux + pool Windows `7590` `7832` `8045` `8373` `10681`; GW Linux + pool Linux `11266` `46317`. La parte Gateway-Linux/Broker-Windows coincide con la plataforma *Nueva* de `sizing.md`; en estos dibujos **no** hay Communication Gateway. | `linux` |
| Recurso Linux | en el Figma lleva un pill `Ubuntu` donde el recurso Windows lleva el `Thinfinity Agent` (`39669`, `46317`). Se copia tal cual; no se deduce nada del producto de ahí. | `linux` |
| Gateway/Broker "dentro de Windows Server" | **no** se dibuja la caja-host; el SO va en el label si el pedido lo dice | — |
| Cruce Brokers → Gateways (2×2) | cada Broker abre hacia **ambos** Gateways (cross-mesh, I1); es la HA estándar | — |
| Bus de retorno | los agentes marcan saliente: bus que sale de la Subnet y entra al Gateway por arriba y por abajo | — |
| Réplica entre sitios | flecha **bidireccional** entre las pills de base de cada sitio | — |

### 6.4 Elegir el escalón desde los "Datos del caso"

Solo cuando el pedido trae el dato; **un campo vacío no se adivina** (regla de "Datos del caso").

| El caso dice | Escalón |
|---|---|
| prueba de concepto, demo, evaluación, pocos usuarios | E1 |
| piloto, "pasar a producción" | E2 |
| hasta ~1000 usuarios, HA | E3 (+ E3b si hay varias redes o varios SO; E3c si hay un sitio secundario) |
| ~1000 a 5000 usuarios, o dos sitios activos a la vez (usuarios en ambos) | E4 |
| dos ubicaciones, una principal y otra secundaria / de respaldo | E3c |
| recuperación ante desastres explícita | E5 |
| nada de lo anterior (form vacío) | diagrama simple estándar: **E2 sin LB si no pide HA**, nunca E4 ni E5 por defecto |

- **Sistema operativo: dos ejes que no se deducen uno del otro.** Gateways (`Windows Server` o `Linux Server`; con Linux, Users trae `Linux Client`) y recursos (`Windows 11`, `Windows Server`, `Linux Server` + `Ubuntu`). Los Brokers van `Windows Server`. Plataforma *Nueva* → Gateways Linux (§6.3). Si el pedido dice solo "Linux", **leer qué es Linux** (¿Gateway, recursos o ambos?) y, si no se sabe, no suponer: Gateway `Windows Server` y rotular los recursos como dice el pedido. El escalón no cambia.
- Los números de usuarios por país o sitio (p. ej. `Perú – 730 Usuarios`) van en el label de la zona, tal
  cual los da el pedido.
- En **modo Advanced** mandan los números de `sizing.md` (cantidad de Gateways, Brokers, Communication
  Gateways); el escalón solo aporta la forma. Si el sizing da más de 3 de algo, vale la regla de `⋮` de
  SKILL §5.1.
- Los frames están duplicados en ES/EN y por SO: son el **mismo** diagrama. Elegir uno; el idioma de los
  labels lo fija el pedido.


### 6.5 Los dos modelos de 2 sitios

Los frames de 2 sitios son **dos modelos distintos**; no mezclarlos:

| | **Activo-Activo** (E4) | **Principal + secundario** (E3c, E5) |
|---|---|---|
| Quién recibe usuarios | **ambos** sitios (cada uno con su `Users`, WAF · Firewall y LB) | solo el **principal**. En E3c el LB del secundario no recibe flecha de usuarios; en E5 el secundario tiene `URL Recovery` como entrada de emergencia |
| Forma del 2.º sitio | **simétrico** al 1.º | **reducido**: 1 Gateway, 1 Broker, 1 base (E3c suma Monitoring Server) |
| Broker del 2.º sitio | solo hacia **sus** Gateways | hacia su Gateway **y** hacia los **2 Gateways del principal** |
| Réplica | flecha vertical bidireccional entre las bases | igual |
| Nodos | `9484` `9908` `13073` `12327` | `10332` `10681` · DR `12614` `12811` |

**Cómo dibujarlos en pills:**

1. **Site 1 arriba, Site 2 abajo, en la misma grilla de columnas** (Users · LB · Gateways · Brokers · bases · Subnet), para que las bases queden una sobre otra y la réplica sea una sola flecha vertical.
2. Etiquetas `Site 1` / `Site 2` en los márgenes y una **línea punteada oscura horizontal** como separador. Como cada sitio lleva una Subnet adentro, **no** se dibuja el sitio como zona (SKILL §2.3 prohíbe anidar): línea + etiqueta.
3. El bus de retorno de cada Subnet entra a los Gateways **de su propio sitio** (arriba y abajo, como en E1–E3).
4. En activo-pasivo, las dos flechas del Broker del Site 2 hacia los Gateways del Site 1 van por un **corredor propio** entre la columna de Brokers y la de Gateways, sin atravesar pills (en el Figma son diagonales; acá, ortogonales).
5. Réplica = flecha bidireccional `<->` con chevrons entre las dos pills de base, cruzando el separador.
6. Site 2 reducido en activo-pasivo: 1 Gateway y 1 Broker **salvo que el caso o Advanced diga otra cosa**.

**Réplica (Nick, 2026-10-27):** que en `10332`, `9484` y `9908` la flecha toque la base Analytics / HeatWave del Site 1 es un **atajo de layout**. Se dibuja entre las bases equivalentes: `MySQL Database` (Profiles) del Site 1 ↔ `MySQL Database` del Site 2. Analytics / HeatWave no se replica en el dibujo.