# Thinfinity Architecture Diagram Skill — Handoff Document

> **Para futuras instancias de Claude**: este documento captura todo el contexto y progreso de un trabajo iniciado por Nick Ceraso (nceraso@cybelesoft.com, Cybele Software). Subilo al iniciar una nueva sesión para retomar exactamente donde quedamos.
>
> **Fecha del último update**: 2026-05-22

---

## 1. Objetivo

Construir un **skill** (para uso interno mío, Claude) que, a partir de un prompt en lenguaje natural, genere un **gráfico de arquitectura del producto Thinfinity** (Cybele Software, Inc.) respetando el sistema visual definido en Figma:

- Iconografía oficial del branding.
- Tamaños fijos de contenedores y átomos.
- Colores brand con tokens documentados.
- Líneas punteadas como sintaxis de "zona/subred".
- Conectores con un estilo y color específicos.

Output esperado: **SVG nativo standalone + HTML preview**, opcionalmente pusheable a Figma vía `mcp__figma-remote-mcp__generate_figma_design`.

---

## 2. Archivos Figma de referencia

| Archivo | fileKey | Rol |
|---|---|---|
| **Exercise** | `8RBfhSYgaCuo4uM82JqAHL` | Spec canónico. Nick limpió el archivo y dejó **5 frames** de muestra con los átomos oficiales (ver §4). |
| **Architecture-Diagrams** | `W3Pnm739iwmVdo3hSaBNQe` | Biblioteca de íconos (131 SVG) + samples reales de diagramas (Architecture sample: Gateway on DMZ, ZTNA, Multi-Tenant, etc.). De acá saqué los íconos. |

URL de referencia del Exercise: `https://www.figma.com/design/8RBfhSYgaCuo4uM82JqAHL/Exercise?node-id=0-1`

### 2.1 Frames canónicos en Exercise (Page `0:1`)

| Frame name | Node ID | Tamaño | Contenido |
|---|---|---|---|
| `Thinfinity Related elements` | `245:38580` | 130×312 | Pills Gateway, Broker, Prim Broker, Sec. Broker, Agent |
| `Users` | `246:38589` | 127×245 | Pills User, Remote User, Browser Client, Local User |
| `Secondary elements (sample)` | `247:38590` | 129×190 | Pills MySQL Data Base, Firewall, Tunnel |
| `Network and subnet elements` | `247:38591` | 127×306 | Pills DASHED: Cloud, On-Prem, Hybrid, DMZ, Network |
| `Connection vector` | `247:38592` | 99×31 | Flecha azul canónica |

---

## 3. Working directory

Todo el trabajo vive en `C:/Users/NickCeraso/thinfinity_arch_skill/`.

```
thinfinity_arch_skill/
├── STYLE_SPEC.md              ← spec canónico (autoritativo)
├── spec_preview.html          ← preview visual de los átomos
├── spec_preview_render.png    ← screenshot del preview
├── test_01_basic.html         ← test 01: Remote User → Gateway ← Broker + Web App
├── test_01_render.png         ← screenshot test 01
├── icons_gallery.html         ← galería de los 131 íconos
├── icons_gallery_render.png   ← screenshot galería
├── icons/                     ← 131 SVG nativos
│   ├── _arrow.svg             ← flecha conector canónica
│   ├── thinfinity.svg         ← flor brand
│   ├── gateway.svg
│   ├── broker.svg
│   ├── firewall.svg
│   ├── ... (128 más)
├── refs/                      ← screenshots de samples del Figma original
│   ├── sample_thinfinity_elements.png
│   ├── sample_users.png
│   ├── sample_secondary.png
│   ├── sample_network.png
│   ├── sample_connection.png
│   └── sample_01..08_*.png    ← samples legacy del file original
├── remaining_icons.txt        ← lista de node IDs (referencia histórica)
└── test_diagrams.html         ← ❌ deprecated (primer intento con íconos dibujados a mano)
```

---

## 4. Style spec canónico

> El archivo autoritativo es `thinfinity_arch_skill/STYLE_SPEC.md`. Lee ese primero. Resumen acá:

### 4.1 Átomo único: la **pill**

Todas las piezas comparten la misma caja. **No hay variación de ancho.**

| Propiedad | Valor |
|---|---|
| Width × Height | **110 × 43 px** |
| Border | **1.5 px solid** (color varía según categoría) |
| Radius | **7 px** |
| Padding | **10 px** todos lados |
| Gap interno | **6 px** entre ícono y label |
| Ícono | **23 × 23 px** |
| Texto | Inter Regular **12 px**, leading normal |
| Background (variantes sólidas) | `#FFFFFF` |

### 4.2 Las 3 variantes sólidas

| Categoría | Stroke + texto | Usos |
|---|---|---|
| **Thinfinity** | `#0A74D6` (Cybele blue) | Componentes Thinfinity (Gateway, Broker, Agent, etc.) |
| **User** | `#373737` (dark) | Actores humanos (User, Remote User, Local User, etc.) |
| **Secondary** | `#BDBDBD` stroke + `#373737` texto | Infra periférica (Firewall, Tunnel, DB, etc.) |

> **CRÍTICO**: las pills Thinfinity son **blancas con stroke azul**, NO tienen fill celeste. Esto es un error que cometí en la primera iteración.

### 4.3 Variantes DASHED (zonas/subredes)

Mismo box pero `border-dashed` + fill semitransparente:

| Zona | Stroke | Fill | Texto | Ícono |
|---|---|---|---|---|
| Cloud | `#2FB18A` | `#E2F7F1` | `#2FB18A` | `cloud` |
| On-Prem | `#8878ED` | `#EDEBFC` | `#8878ED` | `premises` |
| Hybrid | `#0A74D6` | `#CDDDFA` | `#0A74D6` | `hybrid` |
| DMZ | `#BDBDBD` | `#FFFFFF` | `#373737` | `connect` |
| Network | `#BDBDBD` | `#FFFFFF` | `#373737` | `network` |

### 4.4 Connection vector

Usar el asset `icons/_arrow.svg` (viewBox 99×31, fill `#0AA9FF`).

- **Color**: `#0AA9FF` (azul cielo) — **NO** `#0A74D6` (esto fue otro error inicial).
- Stroke ~2 px, arrowhead chevron integrado.
- Routing ortogonal (right-angle bends) cuando hay quiebres.

### 4.5 Palette completa de tokens

| Token | Hex |
|---|---|
| `colors/main` | `#0A74D6` |
| `Thinfinity/500` | `#007DC1` |
| `Thinfinity/50` | `#EFF9FF` |
| `Blue Cybele/50` | `#EFF7FE` |
| `blue/100` | `#CDDDFA` |
| `White/500` | `#FFFFFF` |
| `Grey/300` | `#BDBDBD` |
| `Colors/Typography/title` | `#373737` |
| `color/typography/paragraph` | `#515151` |
| `water-green/500` | `#3DCCA1` |
| `water-green/600` | `#2FB18A` |
| `water-green/100` | `#E2F7F1` |
| `blue-violet/500` | `#8878ED` |
| `blue-violet/100` | `#EDEBFC` |
| `green/600` | `#649B1F` |
| `orange-cybele/500` | `#FAA928` |
| **arrow blue (conector)** | `#0AA9FF` |

---

## 5. Iconografía

**131 SVGs nativos** en `icons/`. Extraídos del archivo Architecture-Diagrams. Cada SVG mantiene su color brand como CSS var con fallback (`var(--fill-0, #0A74D6)` y similares).

### 5.1 Set completo (alfabético)

```
2FA, RDBAC-access-control, VPN-alert, access-location, active-directory,
admin, all-profiles, app, app-group, app-remote, app-server, app-virtual-ui,
app-virtualization, app-web, assign-VM, audit-log, auth0, authenticated-cloud,
aws, azure, broker, broker-monitor, cancel, check, cloud, cloud-azure, cloud-ok,
complex, config-options, connect, daas, database, databases, desktop, duo,
easy-management, email, endpoint-agnostic-access, entra-id, fingerprint, firewall,
forgerock, fslogix, gateway, gear, globe, google, gpu-fast, granular-access,
hacker, html5, hybrid, hyper-v, iaas, iaas-infrastructure, id, identity-federation,
identity-integration, internal-session-brokering, key, layered-security, linux,
load-balancer, location, lock-blank, lock-check, login, management-complexity,
manufacture, monitor-VM, multi-monitor, multi-platform, multi-tenancy, network,
new-app, new-window, notebook, on-premises-management, options, oracle, pc,
pc-star, pc-user-location, perimeter-based, premises, printer, profile, proxy,
publishing, rec, recordings, refresh, remote, remote-access, remote-app,
remote-app-mode, remote-working, roadmap, saas-integration, saml, secure-access,
secure-password, secure-server, server, session-share, shield, shield-ok,
ssh-connection, system-config, terminal, thin-vnc, thinfinity, usability,
user, user-config, user-group, user-guest, user-vm, vdi, view-data, vm, vnc,
vpn, vpn-tunnels, web, web-app, web-cloud, win-app, windows, windows-desktop,
workload
```

### 5.2 Semántica de color en los íconos

Los íconos **traen su propio color codificado** por categoría — preservar al renderizar:

- **Cybele blue `#0A74D6`** → componentes Thinfinity, infra genérica.
- **Thinfinity blue `#007DC1`** → glifo flor (`thinfinity.svg`), `daas`.
- **Dark `#373737`** → firewall, neutros.
- **Water-green `#3DCCA1` / `#2FB18A`** → identity / IDP (active-directory, identity-integration, internal-session-brokering, saas-integration, on-premises-management, iaas).
- **Green `#649B1F`** → security / 2FA / shield / multi-platform / perimeter-based / VPN-alert / vpn-tunnels / layered-security.
- **Blue-violet `#8878ED`** → globe, hacker; zona On-Prem.
- **Orange `#FAA928`** → remote-access alert state.
- **Logos vendor** (`aws`, `azure`, `google`, `duo`, `forgerock`, `oracle`, `entra-id`, `auth0`, `saml`, `html5`, `windows`, `linux`, `hyper-v`) → mantener color brand original.

### 5.3 Issue arreglado en los SVGs

Todos los SVGs venían con `preserveAspectRatio="none"` (causaba deformaciones al renderizar). Lo reemplacé por `preserveAspectRatio="xMidYMid meet"` en los 132 archivos (131 íconos + el `_arrow.svg`).

---

## 6. Cronología del progreso

### Fase 1 — Análisis inicial (errores)
- Pedí mapear el archivo Exercise original (87+ diagramas de arquitectura).
- Analicé 8 samples representativos.
- **Sinteticé un spec con varios errores**: pills variables 110/120/140, fill celeste en pills Thinfinity, radius 6-8, border 1px, font Inter Medium 13, arrow color `#0A74D6`. **TODO ESO ESTABA MAL**.
- Generé `test_diagrams.html` con 2 ejemplos. Nick señaló problemas.

### Fase 2 — Iconografía
- Nick pasó el archivo Architecture-Diagrams (`W3Pnm739iwmVdo3hSaBNQe`).
- Bajé los 131 SVGs nativos de Figma usando `mcp__figma-remote-mcp__get_design_context` (que devuelve URL `image/svg+xml`).
- Armé galería en `icons_gallery.html`.

### Fase 3 — Re-análisis con frames canónicos (corrección)
- Nick limpió el archivo Exercise y dejó **5 frames de muestra** con los átomos canónicos (§2.1).
- Releí esos frames con `get_design_context` y `get_variable_defs`.
- **Recodifiqué el spec con valores exactos** (§4).
- Bajé el arrow real (`_arrow.svg`, fill `#0AA9FF`).
- Arreglé `preserveAspectRatio="none"` en los 132 SVGs.
- Armé `spec_preview.html` materializando los átomos.

### Fase 4 — Primer test diagrama (en curso)
- **Test 01** (`test_01_basic.html`): Remote User → Thinfinity Gateway ← Thinfinity Broker + Web App, con Broker y Web App dentro de una zona Network dashed. Todas las flechas direccionadas AL gateway.
- Esperando feedback de Nick.

---

## 7. Estado — ✅ COMPLETO

```
✅ #1. Map the Figma file structure
✅ #2. Catalog visual rules per diagram
✅ #3. Synthesize style spec
✅ #4. Generate test Thinfinity diagrams        (7 diagramas validados, complejidad creciente)
✅ #5. Iterate on test diagrams with user feedback
✅ #6. Author the skill                          ← HECHO
✅ #7. Extract canonical icons from icon library (131 icons)
✅ #8. Re-analyze Exercise file for precise specs
```

### EL SKILL YA EXISTE
- Ubicación: `C:/Users/NickCeraso/.claude/skills/thinfinity-architecture/`
  - `SKILL.md` — spec + workflow completo (autoritativo)
  - `icons/` — 131 SVG + `_arrow.svg`
  - `reference/` — 7 renders validados + atoms_spec
  - `examples/` — los 7 HTML fuente
- Se invoca solo cuando el usuario pide un gráfico de arquitectura Thinfinity/Cybele.

### 7 diagramas validados (en `thinfinity_arch_skill/`)
1. `test_01_basic.html` — Remote User → Gateway ← Broker + Web App (Network zone)
2. `test_02_hybrid.html` — híbrido Cloud/On-Prem
3. `test_03_full.html` — full ref (uniform pills, compacto)
4. `test_04_multiregion.html` — multi-región **color-coded + dual-flow** (caso excepcional)
5. `test_05_idp_domains.html` — multi-dominio + Thinfinity IDP (conector dashed)
6. `test_06_vdipools_backup.html` — VDI pools + Backup
7. `test_07_managed_hub.html` — hub-and-spoke radial, clouds espejadas

### Reglas nuevas consolidadas en estas 7 pruebas (todas en SKILL.md §1-§10)
- Pill **uniforme 160×43** (no hay variantes de tamaño).
- Categoría solo por **stroke+texto** (Thinfinity azul / User dark / Secondary gris); ícono mantiene su color.
- Zonas dashed, **sin anidar dashed** (flatten); label top-left o badge en esquina (con margen).
- Conector **chevron-stroke `#0AA9FF`** (no triángulo, no `#0A74D6`).
- **Capas: zonas → conectores → pills** (si no, se ocultan los arrowheads).
- **≥14px recto antes de la punta**; arrowheads al mismo elemento **≥14px separados**.
- **Gaps ~43px**; ensanchar solo en zonas de cruce/distribución densas.
- Conector **dashed** = flujo secundario (auth IDP, backup, mgmt).
- **Color-coding = excepción opt-in**; default monocromático.
- Broker dentro de su región; grupos espejados son reflejos limpios.

---

## 8. Preguntas abiertas (necesitan decisión de Nick)

Surgidas en Test 01 (`test_01_basic.html`):

1. **Web App styling** — la styleé como Secondary (border gris). ¿Va o querés Thinfinity-styled (border azul)?
2. **Posición de la pill "Network"** dentro de la zona — la puse top-left adentro como título. ¿Mantener, ponerla afuera arriba, o sentada sobre el borde?
3. **Bus vs flechas separadas** — los conectores Broker→Gateway y Web App→Gateway son 2 flechas ortogonales independientes. ¿Mantener o juntar en un bus único?

Preguntas estructurales más generales (pendientes desde la fase 3):

4. **Contenedores de sección** (las cajas celestes con título tipo "The Gateway", "The Broker" que aparecían en los samples legacy) — ¿siguen vigentes o se descartan?
5. **Sub-cards tipo "Machine"** (cajita blanca con borde gris envolviendo un grupo de pills) — ¿se usa o descartado?
6. **Spacing canónico entre pills apiladas** — observé strides 56-58px en samples del legacy. ¿Lo fijo en 14px de gap?
7. **Bus connectors** (varios users → línea convergente → firewall pill) — ¿pattern oficial o lo armo libre?

---

## 9. Memorias relevantes del usuario (`MEMORY.md`)

Estos hábitos del usuario aplican:

- **Nick Ceraso**, Cybele Software, sin background de programación, comunica en español.
- Cuenta Figma autenticada en `claude.ai Figma` y `figma-remote-mcp`.
- Working directory para designs: `C:/Users/NickCeraso/dashboard/`.
- Workflow design-to-Figma documentado en `~/.claude/projects/.../memory/figma-workflow.md`.
- Brand design rules: `C:/Users/NickCeraso/cybele_deckgen/BRAND_DESIGN_RULES.md`.
- Logo assets: `C:/Users/NickCeraso/cybele_deckgen/brand_assets/`.

---

## 10. Cómo retomar en una nueva instancia

**Paso 1** — Leé este documento y `thinfinity_arch_skill/STYLE_SPEC.md`.

**Paso 2** — Revisá el estado actual de los archivos:
```
ls C:/Users/NickCeraso/thinfinity_arch_skill/
ls C:/Users/NickCeraso/thinfinity_arch_skill/icons/ | wc -l   # debe ser 132 (131 íconos + _arrow.svg)
```

**Paso 3** — Abrí en el navegador:
- `thinfinity_arch_skill/spec_preview.html` (referencia visual del spec)
- `thinfinity_arch_skill/test_01_basic.html` (último test generado)

**Paso 4** — Verificá vs el archivo Figma. Si Nick editó las muestras canónicas, releé los node IDs en §2.1 con `mcp__figma-remote-mcp__get_design_context`.

**Paso 5** — Resolvé las 7 preguntas abiertas (§8). Solo después de eso, codificá el skill.

**Paso 6** — Cuando estés listo para el skill: el formato esperado es **SVG nativo standalone + HTML preview**, con todos los íconos inlineados como `<symbol>` defs. Skill directory típico: `~/.claude/skills/thinfinity-architecture/`. Mirá `cybele-blog-visuals` como referencia de estructura de skill multi-fase.

---

## 11. Pitfalls a evitar

Errores que cometí en la primera iteración — no repetirlos:

1. **No inferir colores**. Si un valor no está en `get_variable_defs` o en el design context, pedirlo a Nick antes de inventar.
2. **No asumir variantes de tamaño**. Las pills son **siempre** 110×43. No hay 120×43 ni 140×43.
3. **No fills celestes en pills Thinfinity**. Son blancas con stroke azul.
4. **El conector es `#0AA9FF`**, no `#0A74D6`. Y usa el asset `_arrow.svg` o replicalo exactamente.
5. **Cuando importes íconos, no uses `preserveAspectRatio="none"`**. Eso los deforma.
6. **El idioma de los labels** sigue al prompt. Default inglés (matchea las muestras).

---

## 12. Comandos útiles

```powershell
# Abrir el spec preview en el navegador
Start-Process 'C:\Users\NickCeraso\thinfinity_arch_skill\spec_preview.html'

# Re-renderizar headless con Edge
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  --headless --disable-gpu --hide-scrollbars --window-size=1100,600 `
  --screenshot="C:\Users\NickCeraso\thinfinity_arch_skill\test_01_render.png" `
  "file:///C:/Users/NickCeraso/thinfinity_arch_skill/test_01_basic.html"

# Listar íconos disponibles
ls C:/Users/NickCeraso/thinfinity_arch_skill/icons/
```

---

**FIN DEL HANDOFF.**

Si algo no está claro, primero leé `STYLE_SPEC.md`. Si seguís sin entender, preguntale a Nick.

---

## 13. Update 2026-06-16 — estudio del Figma oficial + catálogo de topologías

Se estudió a fondo el archivo oficial **Architecture-Diagrams** (`W3Pnm739iwmVdo3hSaBNQe`) — ~60 diagramas reales, incluyendo despliegues de clientes (Entel, Claro, Rimac, Banco Estado, Telefónica, Oracle Perú). Resultados incorporados al skill:

- **`reference/official_figma_catalog.md` (nuevo)** = fuente de verdad de topologías: índice con node IDs de cada diagrama, vocabulario nuevo (pills `Thinfinity Agent`/`Virtualization Process`/`WAG`/`Load Balancer/WAF`/token pills/`Unique Remote ID`/cables `TLS 1.3 Port 443` y `No Inbound Port`/`MySQL Data Base`/`FSLogix`…), catálogos IDP (11 providers) y conector→target, convenciones visuales nuevas (motif lupa host+burbuja, elipsis `⋮`/`•••` de scale‑out, ejes propiedad×ubicación para On‑Prem/Hybrid/Fully‑Hosted/BYOD, perímetro como líneas dashed en clientes, board multi‑variante V1/V2/V3), y **recetas R12–R33**.
- **`reference/thinfinity_reference_architecture.md`** apunta al catálogo (§6/§8), suma capability→topology para R33 (zero inbound / remove the inbound listener / reemplazo SSL‑VPN), y promueve a 🟢 varios invariantes antes 🟡 (multi‑región, HA/failover, OT reverse‑only) ahora corroborados por el Figma oficial.
- **`SKILL.md`** carga el catálogo en el paso obligatorio de contexto, agrega §5.1 (convenciones extendidas) y actualiza provenance.
- **Ejemplo nuevo de primera clase:** `examples/test_08_zero_inbound_ztna.html` + `reference/ex08_zero_inbound_ztna.png` (R33 — Zero Inbound Ports / ZTNA on OCI). Calibración ahora = **8 diagramas**.
- **Hallazgo clave:** ningún diagrama oficial ni de cliente usa color‑coding por protocolo → los clientes son monocromo azul; el color‑coding sigue siendo excepción opt‑in.
- **Gaps de íconos detectados** (usar fallback): Pump/Motor (`manufacture`), WAF (`shield`), Palo Alto (`firewall`), Nginx (`proxy`), Okta/Jumpcloud/PingID/Onelogin (`id`/`saml`), Dynamics/Wordpress/ERP (`web-app`).
