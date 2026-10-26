# Thinfinity reference architecture — product knowledge (capa 3)

> Este documento es la **capa de producto** que complementa al `SKILL.md` (capa de **cómo** dibujar) y a
> los ejemplos `examples/test_0X.html` (capa de **qué** se ve). Sirve para responder prompts
> **conceptuales** ("acceso remoto seguro a OT", "multi-región VDI") derivando la topología antes de
> dibujar, en lugar de adivinarla.
>
> **Cómo se usa:** después de cargar `SKILL.md` y antes de planear el layout (§9 step 1), consultar este
> documento cuando el prompt habla en términos de **capacidades de producto** (no de componentes
> concretos). De acá salen: componentes → zonas → invariantes que aplican → flujos → receta más cercana.

---

## 1. Catálogo de componentes (rol → pill)

Cada componente mapea a UNA pill canónica de 160×43 (SKILL §1). La categoría (color de borde+texto) ya
está fijada en `SKILL.md §1.1`: **Thinfinity = azul `#0A74D6`**, **User = dark `#373737`**,
**Secondary = gris `#BDBDBD`**.

### 1.1 Componentes Thinfinity core (categoría Thinfinity, azul)

| Componente | Label típico | Icono | Rol | Dónde vive |
|---|---|---|---|---|
| **Gateway** 🟢 | `Thinfinity / Gateway` | `gateway` | Punto de entrada público; reverse-proxy. Único componente expuesto. | DMZ o Cloud |
| **Communication Gateway** 🟡 | `Comm Gateway / <Región>` | `gateway` | Relay de sesión regional (solo multi-región). | dentro de cada región |
| **Primary Broker** 🟢 | `Primary / Broker` o `Thinfinity / Broker` | `broker` | Brokering de sesiones; orquesta a qué recurso va cada usuario. | red corporativa / interna |
| **Secondary Broker** 🟢 | `Thinfinity / Sec. Broker` o `Broker 2` | `broker` | Réplica HA / por región / relay en OT DMZ. | junto al Primary, por región, o en plant edge |
| **IDP** 🟢 | `Thinfinity / IDP` | `thinfinity` (flor) | Proveedor de identidad propio de Thinfinity. | zona IDP Integration |
| **Agent** 🟡 | `Thinfinity / Agent` | `thinfinity` | Se instala en el recurso; lo registra contra el Broker (conexión saliente). | sobre cada recurso |

### 1.2 Endpoints (categoría User, dark)

| Componente | Label típico | Icono | Notas |
|---|---|---|---|
| **Browser / Client / PWA** 🟢 | `Web Browser / Client / PWA`, `Browser Users / HTML5 · TCP 443` | `html5` | Endpoint canónico de Thinfinity: **sin instalar cliente**. |
| **Desktop / Native client** 🟡 | `Desktop Users / Native · HTTPS` | `desktop` | Cliente nativo opcional (cuando el usuario lo requiere). |
| **User / End User / Remote / Local** 🟢 | `User`, `End User`, `Remote User`, `Local User`, `User n` | `user`, `remote`, `user-group` | Actor humano genérico. `User n` para indicar "muchos". |
| **Vendor / Contractor / OEM** 🟡 | `Vendors / OEMs`, `Contractors`, `Employees` | `user-group`, `remote`, `user` | Personas diferenciadas por rol — empleados internos, contractors externos, OEMs/vendors. |

### 1.3 Recursos de backend (categoría Secondary, gris)

| Recurso | Label típico | Icono | Capacidad que representa |
|---|---|---|---|
| Escritorios y apps virtuales 🟢 | `Virtual Desktops / & Virtual Apps` | `vm` / `vdi` | VDI / DaaS |
| Application Servers 🟢 | `Application / Servers` | `app-server` | apps publicadas |
| Terminal Servers 🟢 | `Terminal Servers / & Web Apps` | `terminal` | RDS / web apps |
| Office / Physical Desktops 🟢 | `Office / Desktops`, `Physical / Desktops` | `desktop` | acceso a PCs físicas |
| Windows / Linux Servers 🟢 | `Windows / Server`, `Linux / Servers` | `windows`, `linux` | backends por plataforma |
| VDI Server (pool) 🟢 | `VDI Server`, `VDI Pool A/B / Multi-session` | `server`, `vdi` | nodo o pool VDI multi-session |
| Backup / Database 🟢 | `Backup`, `MySQL Data Base`, `Config DB / (HA) · MySQL`, `Analytics DB`, `Profile DB` | `database` | DR / persistencia / config / telemetría |
| **Task / Knowledge / Engineering Desktops** 🟡 | `Task Desktops · Pooled · stateless` / `Knowledge · Pooled · profiles` / `Engineering · GPU · dedicated` | `vdi` / `vm` / `gpu-fast` | Workload-class separation (ver I13). |
| **MES / SCADA / PLC** 🟡 | `MES System · Line A`, `SCADA / PLC · Line B`, `Windows SCADA · RDP`, `Linux HMI · VNC · SSH`, `Legacy Terminal · TN5250 · Telnet` | `manufacture`, `monitor-VM`, `windows`, `linux`, `terminal` | OT systems detrás del Secondary Broker en plant edge. |
| **FSLogix Profiles** 🟡 | `FSLogix Profiles · SMB` | `fslogix` | Almacén SMB de perfiles para pools VDI. Distinto de Profile DB (MySQL). |
| **Victoria Metrics** 🟡 | `Victoria / Metrics` | `broker-monitor` | Sink de telemetría del Broker (HTTPS :8429). |
| **OCI Object Storage** 🟡 | `OCI Object / Storage / NFS` | `database` | Sink de session recordings con retention inmutable. |

### 1.4 Infra periférica (categoría Secondary, gris)

| Componente | Label típico | Icono | Rol |
|---|---|---|---|
| **TLS tunnel** 🟢 | `TLS 1.3 / Port 443`, `TLS 1.3 / No Inbound`, `TLS 1.3 Traffic` | `vpn-tunnels` | Marca el transporte seguro. `Port 443` en la entrada, `No Inbound` en la salida del broker. |
| Firewall 🟡 | `Firewall` | `firewall` | Perímetro (opcional, pass-through). |
| **Cloud Load Balancer** 🟢 | `Cloud Load / Balancer`, `OCI Flexible Load Balancer` | `load-balancer` | LB en DMZ que distribuye a Gateways duales. |
| **Reverse Proxy** 🟢 | `Gateway 1 / Reverse Proxy`, `Gateway 2 / Reverse Proxy` | `gateway` | Descriptor del rol del Gateway. |
| **SIEM** 🟡 | `SIEM / CEF · JSON`, `Splunk`, `IBM QRadar` | `audit-log`, `layered-security` | Sink de logs en formato CEF/JSON. |
| **Datadog** 🟡 | `Datadog` | `broker-monitor` | Observability unificada IT + OT. |
| **Dragos / Claroty** 🟡 | `Dragos / Claroty` | `layered-security` | OT-specific visibility, correlaciona con Datadog. |

### 1.5 IDPs externos y PAM (categoría Secondary o tintada al flujo; iconos mantienen color de marca)

| Componente | Label típico | Icono | Notas |
|---|---|---|---|
| Active Directory 🟢 | `Active / Directory`, `RWDC-DNS-GC` | `active-directory` | El más común; categoría gold cuando hay color-coding (flujo Directory). |
| Entra ID / Azure AD 🟡 | `Entra ID`, `Federated IdP / SAML · OIDC · MFA` | `entra-id` | Cloud IdP federado. |
| Okta / Auth0 / SAML / ForgeRock / Google / Duo 🟡 | varios | `auth0`, `saml`, `forgerock`, `google`, `duo` | Federación SAML/OIDC. |
| **CyberArk / BeyondTrust** 🟡 | `CyberArk / BeyondTrust` | `lock-check` o `key` | PAM layer entre IdP y Thinfinity para Level 1 OT. |
| **ServiceNow / ITSM** 🟡 | `ServiceNow`, `ITSM / JIT` | `easy-management`, `options` | ITSM que dispara JIT vía webhook al Thinfinity API. |

---

## 2. Catálogo de zonas (dashed containers)

| Zona | Label típico | Icono | Tier que representa | Color |
|---|---|---|---|---|
| **Edge / Internet** 🟢 | `Edge / Internet`, `Vendor (Internet)` | `remote-access` | endpoints externos | gris |
| **Remote Access** 🟢 | `Remote Access` | `remote-access` | endpoints remotos | gris |
| **Local Network** 🟢 | `Local Network` | `network` | endpoints locales | gris |
| **IDP Integration / IDP / SSO** 🟢 | `IDP Integration`, `IDP / SSO`, `Identity Provider`, `Identity & Trust` | `id` | tier de identidad | gris (o magenta cuando hay color-coding SAML) |
| **AD / Identity** 🟢 | `AD / Identity` | `active-directory` | tier de directorio | gris (o gold cuando hay color-coding) |
| **PAM / Privileged Access** 🟡 | `Privileged Access` | `key`, `lock-check` | PAM layer | gris (o gold cuando hay color-coding) |
| **ITSM / JIT** 🟡 | `ITSM / JIT` | `easy-management`, `options` | ITSM/Approvals | gris (o verde cuando hay color-coding) |
| **DMZ** 🟢 | `DMZ`, `Cloud or DMZ`, `IDMZ / OCI` | `connect`, `cloud` | tier del gateway | gris |
| **OT DMZ** 🟡 | `OT DMZ` | `connect` | gateway tier dentro de OT | gris |
| **Corporate / Internal Network** 🟢 | `Corporate Network`, `Internal Network` | `premises` | tier de recursos | gris (dentro del entorno on-prem verde, si se dibuja — SKILL §2.2b) |
| **Corporate Domain · Network N** 🟢 | `Corporate Domain · Network 1…n` | `premises` | un dominio en multi-dominio | gris |
| **Control Plane** 🟡 | `Control Plane` | `broker` | brokers + storage + observability | gris |
| **OCI Cloud** 🟡 | `OCI Cloud` | `cloud` | sitio cloud OCI con ZTNA + Orchestration + Compute | gris |
| **VDI Network** 🟡 | `VDI Network` | `network` | pools VDI + FSLogix | gris |
| **Plant A / Plant B** 🟡 | `Plant A`, `Plant B` | `premises`, `manufacture` | per-planta OT con Secondary Broker + OT systems | gris |
| **OT Network** 🟡 | `OT Network` | `manufacture`, `network` | planta + assets multi-protocolo | gris |
| **Observability & Audit / Governance** 🟡 | `Observability & Audit`, `Observability & Governance` | `audit-log`, `broker-monitor` | telemetry + recordings + SIEM + compliance | gris |
| **Cloud** 🟢 | `Cloud` (o badge en esquina) | `cloud` | sitio cloud genérico | entorno nube: violeta `#8878ED` sobre `#F9F8FE` (SKILL §2.2b; antes verde `#2FB18A`, corregido 2026-09-28) |
| **On-Prem** 🟢 | `On-Prem` | `premises` | sitio on-prem | entorno cliente/on-prem: verde `#3DCCA1` sobre `#F5FCFA` (SKILL §2.2b; antes morado, corregido 2026-09-28) |
| **Región** 🟢 | `Americas`, `Europe`, `Asia` | `globe` (tintado) | banda regional (multi-región) | color por región |

> Regla dura del `SKILL.md` §2.3: **no anidar dashed dentro de dashed**. Pools / subnets / dominios
> dentro de una zona = filas de pills con etiqueta de texto, no cajas internas.

---

## 3. Invariantes del producto (no negociables)

| # | Invariante | Estado | Evidencia / efecto en el diagrama |
|---|---|---|---|
| I1 | **Conexión inversa / sin puertos entrantes.** Broker y recursos *marcan hacia afuera* (dial-out) al Gateway. | 🟢 | Flechas apuntan **hacia el Gateway**; pill `TLS 1.3 No Inbound`; caption `No Inbound Port Required`. |
| I2 | **El Gateway es el único componente público.** Vive en la DMZ o Cloud. | 🟢 | Gateway siempre en DMZ/Cloud, entre endpoints y red corporativa. |
| I3 | **El Broker vive en red corporativa/interna**, junto a los recursos. | 🟢 | Broker dentro de Corporate/Internal Network. |
| I4 | **El acceso es por navegador, sin cliente** (HTML5/PWA). | 🟢 | Endpoint = `Web Browser / Client / PWA`. |
| I5 | **Los recursos están detrás del Broker**; el Agent en cada recurso se registra al Broker. | 🟢 | Recursos → flecha → Broker (bus por fila). |
| I6 | **HA = Primary Broker + uno o más Secondary Brokers.** | 🟢 | Primary central + Sec. Broker por región (test_04) o pair-wise GW+Broker (vdi_pools_ha). |
| I7 | **Transporte = TLS 1.3 / 443.** | 🟢 | Pills tunnel en entrada/salida (test_05, test_06). |
| I8 | **Multi-región:** un Gateway + Primary Broker central; por región Comm Gateway + Sec. Broker + recursos. Plano de control azul separado del plano de sesión coloreado por región. | 🟢 | test_04 (color-coded opt-in). |
| I9 | **Multi-dominio:** un Gateway; por dominio una zona con su Primary Broker + recursos. | 🟢 | test_05. |
| I10 | **Integración de identidad:** IDP propio (`Thinfinity IDP`) o externos (AD/Entra/Auth0/SAML…). Flujo de auth dashed (monocromo) o color magenta (color-coded). | 🟢 | test_05. |
| I11 | **Híbrido = Cloud + On-Prem** coexistiendo. | 🟢 | test_02. |
| I12 | **Managed / DaaS hosted:** header pill `Managed by Cybele Software` + hub-and-spoke. | 🟢 | test_07. |
| **I13** | **Separación obligatoria por workload class.** No colapsar todos los usuarios en un único pool VDI. Task (pooled stateless) / Knowledge (pooled con profiles) / Engineering (dedicated o GPU). | 🟡 | Manufacturing VDI 6-layer; OCI compute shapes permiten sizing por pool. |
| **I14** | **OT reverse-only como safety boundary.** Extiende I1: toda flecha que cruza la frontera OT apunta **outbound**. Firewalls de planta cerrados por default. | 🟡 | Vendor access OT; Manufacturing VDI 6-layer. |
| **I15** | **Identity-driven access, no network trust.** El usuario es la única fuente de confianza; ubicación de red/dispositivo/planta = contexto NO confiable. | 🟡 | Manufacturing VDI 6-layer (capa Identity & Trust). |
| **I16** | **Session containment.** Cada sesión aislada — credencial comprometida ≠ lateral movement a OT. | 🟡 | Vendor access OT; no hay flecha "vendor → red OT" directa. |
| **I17** | **Time-bound + JIT vía ITSM.** Access policies de Thinfinity alimentadas por tickets `Approved`; ticket `Closed` ⇒ access disabled. Integración por webhook al Thinfinity API. | 🟡 | Vendor access OT con ServiceNow. |
| **I18** | **PAM opcional sobre IdP** para Level 1 OT (dual authorization, vaulting, check-in/out). | 🟡 | Vendor access OT con CyberArk/BeyondTrust. |

---

## 4. Semántica de los conectores (qué significa cada línea)

| Línea | Significado | Estado |
|---|---|---|
| **Sólida azul `#0AA9FF` con chevron** | Flujo principal de datos/sesión. Apunta al Gateway (I1). | 🟢 |
| **Dashed azul (`5 4`, sin punta)** | Flujo secundario: **auth (IDP→Broker)**, management, backup. *Modo monocromático.* | 🟢 |
| **Color por flujo (sólido con chevron)** | Plano de sesión por región/tenant/protocolo. **Opt-in** (`SKILL.md §8`). Plano de control queda azure por default. | 🟢 |
| **Bus convergente** | N orígenes → 1 destino con UNA punta. Líneas de entrada sin punta unen al bus. | 🟢 |
| **Bus distribuidor / bifurcación** | 1 origen → N destinos con N puntas. Tronco sin punta, ramas con punta. | 🟢 |

**Paleta sugerida por flujo** (color-coding opt-in, ver `SKILL.md §8` + handoff §12.5 + §13.4):

| Flujo | Color | Aplicación típica |
|---|---|---|
| Sesión / HTTPS 443 | `#0AA9FF` azure | usuario → gateway → broker → recurso |
| Observability / HTTPS 8429 | `#06B6D4` teal | Broker → Victoria Metrics; Dragos/Claroty → Datadog |
| Storage / MySQL 3306 | `#FF7043` naranja | Broker → Config DB / Analytics DB / Profile DB |
| FSLogix profiles / SMB 445 | `#06B6D4` teal | VDI Pools → FSLogix (puede compartir teal con observability si no coexisten) |
| SSO / SAML 2.0 | `#EC4899` magenta | IdP (Entra/Okta) → Broker / ZTNA Gateway |
| Directory / LDAP-Kerberos-DNS-SMB-RPC | `#F59E0B` amber/gold | Broker / VDI agents → AD |
| PAM workflow | `#F59E0B` gold (o variante) | CyberArk/BeyondTrust → IdP |
| ITSM / JIT | `#43A047` verde | ServiceNow → Thinfinity API |
| Audit / recordings | `#FF7043` naranja (compartido con storage) | Broker → OCI Object Storage; GW → SIEM |

---

## 5. Mapa CAPACIDAD → TOPOLOGÍA

| Si el prompt dice… | …el skill instancia |
|---|---|
| "acceso por navegador / sin cliente / zero-install / clientless" | pill `Web Browser / Client / PWA` |
| "acceso remoto seguro / ZTNA / sin VPN" | zona Remote Access → Gateway en DMZ → conexión inversa (I1) |
| "sin abrir puertos / sin tocar el firewall / no inbound" | flechas recurso/broker→gateway + pill `TLS 1.3 No Inbound` + caption `No Inbound Port Required` |
| **"zero inbound ports / remove the inbound listener / reemplazo de SSL-VPN (FortiGate/FortiOS) / sin VPN portal / sin 3389"** | **R33** (catálogo oficial §4): navegador → Gateway "Edge · No Listener"; subnets privados con `Thinfinity Agent` que marcan saliente (Agent→Broker→`Outbound-only TLS / No Inbound Port`→Gateway); Identity·MFA con auth al Gateway. Todo el lado privado apunta al Gateway. |
| "publicar aplicaciones / RemoteApp / apps Windows" | `Application Servers` / `Terminal Servers & Web Apps` |
| "escritorios virtuales / VDI / DaaS" | `Virtual Desktops & Virtual Apps` / `VDI Pool A/B · Multi-session` |
| "acceso a PCs físicas / oficina" | `Office Desktops` / `Physical Desktops` |
| "balanceo / brokering de sesiones" | `Primary Broker` |
| "alta disponibilidad / failover / redundancia" | `Primary Broker` + `Secondary Broker` (I6); pair-wise GW+Broker si el usuario menciona pares |
| "SSO / MFA / 2FA / federación de identidad" | IDP (`Thinfinity IDP` o externos) + flujo dashed (mono) o magenta (color-coded) de auth (I10) |
| "multi-región / global / baja latencia" | por región: `Comm Gateway` + `Sec. Broker` + recursos; color-coded (I8) |
| "multi-dominio / multi-tenant" | por dominio: zona con `Primary Broker` + recursos (I9) |
| "híbrido / nube + on-premise" | zona `Cloud` + zona `On-Prem` (I11) |
| "gestionado por Cybele / DaaS hosteado" | header `Managed by Cybele Software` + hub-and-spoke (I12) |
| "backup / disaster recovery" | pill `Backup` (icono `database`) |
| "Windows y Linux" | iconos `windows` + `linux` en los recursos |
| **"acceso de vendors / contractors / OEMs a OT"** | personas diferenciadas (`Vendors`, `Contractors`, `Employees`) + IdP federado + PAM + ITSM/JIT + ZTNA Gateway + Secondary Broker en OT DMZ + assets multi-protocolo (RDP/VNC/SSH) + audit/recording + session containment (I14, I16, I17, I18) |
| **"manufacturing VDI / planta / multi-plant"** | 6-layer: Identity & Trust + Users (3 personas) + OCI (ZTNA + Orchestration + 3 pools por workload class) + Plants × N (Sec Broker + OT systems) + Observability (I13, I14, I15) |
| **"workload separation / pooled vs dedicated / GPU engineering"** | 3 pools separados: Task (pooled stateless) + Knowledge (pooled con profiles) + Engineering (dedicated o GPU) (I13) |
| **"session telemetry / observability / Datadog / Dragos / Claroty"** | Datadog pill + Dragos/Claroty pill en zona Observability & Audit; flechas teal de Broker → Datadog y Dragos/Claroty → Datadog |
| **"compliance / IEC 62443 / NIS2 / ISO 27001 / NIST"** | pills en zona Observability & Governance: `Audit Logs · Forensic`, `SIEM · CEF/JSON`, `ISO 27001 · NIST · Compliance` |
| **"session recording"** | pill `OCI Object Storage` (cloud, immutable retention) o `NFS write-protected` (on-prem) |
| **"JIT / ServiceNow / approvals workflow"** | pill `ServiceNow` en zona ITSM/JIT + flecha verde → Thinfinity API en Gateway |
| **"PAM / CyberArk / BeyondTrust / privileged access"** | pill `CyberArk / BeyondTrust` en zona Privileged Access + flecha gold → IdP (workflow check-in/out) |
| "endpoint-agnostic / cualquier dispositivo" | refuerza endpoint browser; no agrega componente |

---

## 6. Recetas de topología (catálogo)

| Receta | Patrón | Cuándo usarla | Ejemplo fuente |
|---|---|---|---|
| **R1 — Básica** 🟢 | Remote User → Gateway ← Broker + recurso (en zona Network) | demo mínima, "cómo funciona" | `examples/test_01_basic.html` |
| **R2 — Híbrida** 🟢 | Users (bus) → Cloud(Gateway) ← On-Prem(Broker + server) | nube + on-prem | `examples/test_02_hybrid.html` |
| **R3 — Referencia completa** 🟢 | Remote + Local users → Gateway (DMZ) → Broker (Corp) → bus vertical → todos los tipos de recurso + Cloud VDI | "arquitectura de referencia / todo el producto" | `examples/test_03_full.html` |
| **R4 — Multi-región** 🟢 | Gateway+Primary Broker central → por región Comm Gateway + Sec. Broker + recursos; **color por región** | global, baja latencia | `examples/test_04_multiregion.html` |
| **R5 — Multi-dominio + IDP** 🟢 | un Gateway; por dominio zona con Primary Broker + recursos; `Thinfinity IDP` con auth dashed | varios dominios/tenants con identidad | `examples/test_05_idp_domains.html` |
| **R6 — VDI pools + Backup** 🟢 | zona IDP Integration → Gateway → Primary Broker(s) → Internal Network con pools VDI (subnets) + Backup | DaaS con pools y DR | `examples/test_06_vdipools_backup.html` |
| **R7 — Managed hub-and-spoke** 🟢 | header `Managed by Cybele`; Gateway central; spokes cloud (Broker+recursos) espejados | servicio gestionado/DaaS hosteado | `examples/test_07_managed_hub.html` |
| **R8 — Cloud VDI + LB + brokers HA** 🟡 | Users (Browser/Desktop) → Cloud LB (DMZ) → Gateways duales; Brokers HA y VDI pools marcan inversa a ambos gateways vía bus colector; FSLogix (SMB) en VDI Network; Config DB (MySQL); AD con fan-out a brokers + Config DB + pools | despliegue VDI en cloud con LB y HA | `oci_vdi_arch.html` |
| **R9 — Cloud VDI con stack completo + paleta por protocolo** 🟡 | R8 + Victoria Metrics + Analytics DB + Profile DB + SSO IdP externo (SAML) además de AD. Convergencia explícita HTML5→LB, bifurcación explícita LB→GWs y AD→VDIs. Color-coding por protocolo (5 colores). | despliegue VDI con TODOS los flujos discriminados | `oci_vdi_thinfinity_v2.html` |
| **R10 — Zero-trust vendor access OT** 🟡 | Identity (IdP + PAM + ITSM) → ZTNA Gateway (IDMZ/OCI) → Secondary Broker (OT DMZ, reverse) → multi-protocol OT assets (RDP/VNC/SSH-Telnet). Observability + recordings + SIEM bottom. **6 colores**. | acceso de terceros (OEMs/contractors) a sistemas OT con audit/compliance estricto | `ot_vendor_access_arch.html` |
| **R11 — Manufacturing VDI 6-layer (OCI)** 🟡 | Identity & Trust (top) + Users (3 personas) + OCI Cloud (ZTNA + Orchestration + 3 Compute pools por workload class) + Plants × N (Sec Brokers + OT systems) + Observability & Governance (bottom). Convergencia inward de users, outward de plantas — ambas en el ZTNA Gateway. | despliegue completo VDI manufacturero con governance ISO/NIST | `manufacturing_vdi_oci_arch.html` |

> **R12–R32 (catálogo oficial de Figma) 🟢** viven en `reference/official_figma_catalog.md` §4 —
> son las topologías **nombradas** del archivo oficial de Cybele, todas respaldadas por diagramas reales:
> Single Machine (R12), Gateway/Broker split (R13/R13b), GW-Broker Separation (R14), modelos de propiedad
> On-Prem/Hybrid/Fully-Hosted/BYOD (R15), single-tenant server farm (R16), Single Datacenter HA (R17), las
> variantes de Load Balancing (R18/R19/R20/R21), Failover/DR (R22), Multiple Networks (R23), Multi-Domain
> Multi-Tenant Hybrid (R24), Multi-Tenant por plataforma/cliente (R25a/b), Single-DB compartida (R26/R27),
> RBAC (R28), Behind Palo Alto (R29), Connect IT/OT (R30), OT & Offline (R31), WAG (R32) + la plantilla
> "Detailed IDP Integration" y los patrones de clientes reales (DR dual-site, gateways internal/external,
> fan-out de gateways, FSLogix). **Para una topología nombrada o ambigua, buscá primero en ese catálogo y
> abrí su nodeId en Figma para calibrar** antes de elegir entre R1–R11.

---

## 7. Cómo se expande un prompt conceptual (workflow)

1. **Identificar capacidades** en el prompt (acceso por navegador, multi-región, OT, JIT, etc.).
2. **Mapear cada capacidad** a componentes via §5 (CAPACIDAD → TOPOLOGÍA).
3. **Aplicar invariantes** automáticamente (§3), aunque el usuario no los mencione:
   - I1, I2, I3 siempre.
   - I4 si el endpoint es usuario (no programático).
   - I6 si menciona HA / redundancia / failover.
   - I8 si menciona multi-región.
   - I9 si menciona multi-dominio / multi-tenant.
   - I10 si menciona auth / SSO / MFA.
   - I11 si menciona híbrido / nube + on-prem.
   - I12 si menciona managed / DaaS hosteado.
   - I13, I14, I15, I16, I17, I18 si menciona OT / manufacturing / vendor / contractor.
4. **Elegir la receta** más cercana de §6 (puede ser una variante de R3, R8, R10, R11…).
5. **Renderizar** siguiendo `SKILL.md §9` (incluyendo footer §11 + pre-render check §12).

> Si el prompt es **ambiguo en un invariante** (ej. no se sabe si quiere HA), el skill **elige el default
> del producto** (un solo Primary Broker) y lo menciona — en vez de preguntar por cada detalle. Solo
> preguntar si la elección cambia sustancialmente el diagrama (ej. ¿single-region o multi-region?).

---

## 8. Punteros

- **Catálogo oficial de Figma (FUENTE DE VERDAD de topologías):** `reference/official_figma_catalog.md`
  — índice de ~60 diagramas reales con node IDs (fileKey `W3Pnm739iwmVdo3hSaBNQe`), vocabulario nuevo
  (componentes/zonas/labels), convenciones visuales extendidas y recetas R12–R32. Consultar para cualquier
  topología nombrada/ambigua y calibrar abriendo el nodeId en Figma.
- **Capa visual (CÓMO):** `SKILL.md` en la raíz del skill — la autoridad.
- **Ejemplos validados:** `examples/test_0X.html` (7) + `reference/ex0X_*.png`.
- **Iconos:** `icons/` (131 SVGs + `_arrow.svg`).
- **Backstory + open notes:** `thinfinity_arch_skill_handoff.md` (v1) y `_v2` (extiende v1 con
  §11/§12/§13: routing fino, color-coding, reference footer, pre-render check), más `STYLE_SPEC.md`.
  **Viven fuera de este repo** y no son insumos: lo necesario para dibujar está en esta carpeta. Si te
  mandan a leer uno y no se puede abrir, decilo y seguí con lo que está acá.
- **Artefactos generados (validación visual de la capa 3):**
  - `oci_vdi_arch.html` (R8), `oci_vdi_thinfinity_v2.html` (R9), `ot_vendor_access_arch.html` (R10),
    `manufacturing_vdi_oci_arch.html` (R11), `vdi_pools_ha_arch.html` (variante R9 con HA pair-wise).
  - `zero_inbound_ztna_oci.html` (**R33** — Zero Inbound Ports / ZTNA clean sobre OCI; ver catálogo
    oficial §4 R33). Patrón: navegador → TLS 443 → Gateway "Edge · No Listener"; Identity·MFA con auth
    punteada al Gateway; subnets privados OCI con VDI/App + `Thinfinity Agent` que marcan **saliente**
    (Agent → Broker → `Outbound-only TLS / No Inbound Port` → Gateway). Todo el lado privado apunta al
    Gateway = cero puertos entrantes. Útil para prompts de "remove the inbound listener", reemplazo de
    SSL-VPN (FortiGate/FortiOS) y guías ZTNA.

---

**Estado del documento:**
- 🟢 = respaldado por ≥1 de los 7 ejemplos canónicos **o por el catálogo oficial de Figma**
  (`reference/official_figma_catalog.md`).
- 🟡 = inferencia desde el producto Thinfinity / sesiones de trabajo con Nick; usar como guía con
  awareness de que falta confirmación formal.
- Los pendientes 🟡 se resuelven validando con Nick y promoviéndolos a 🟢.
- **Actualización (catálogo oficial):** el Figma oficial corrobora varios invariantes antes 🟡 —
  multi-región (I8: `428:4136`, `428:4152`), HA/failover (I6: `428:4155`, `429:4393`), y la frontera
  OT reverse-only (I14: `428:4092`, `428:4077`). El color-coding por protocolo (§4 paleta, R9/R10/R11)
  **no aparece en ningún diagrama oficial ni de cliente** — sigue siendo feature idealizado opt-in.
