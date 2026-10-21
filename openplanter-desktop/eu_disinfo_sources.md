# Principales bases de datos y fuentes sobre desinformación/misinformación (UE + Estados miembros)

**Fecha de recopilación (UTC):** 2026-09-14T11:04:49Z (ver `evidence/retrieval_utc.txt`).

## Metodología (breve)
1. Priorización de portales **institucionales de la UE**, observatorios paneuropeos financiados/respaldados por la UE y fuentes nacionales de Estados miembros.
2. Verificación técnica: cuando fue posible, se comprobó acceso con `curl` y se guardaron artefactos en `evidence/` (HTML/headers) para cita reproducible.
3. Limitaciones: algunos sitios bloquean automatización (Cloudflare/WAF/antivirus en red) y no permiten verificación completa desde este entorno.

---

## 1) Unión Europea (nivel UE) — fuentes principales

### A. **DSA Transparency Database (Comisión Europea)**
- **Qué es:** base/portal de transparencia exigida por la Digital Services Act; permite explorar y descargar información que las plataformas deben publicar.
- **URL:** https://transparency.dsa.ec.europa.eu/
- **Evidencia (capturada):** título HTML “Home - DSA Transparency Database” (ver `evidence/dsa_home.html`).
- **Notas:** Aunque no es “solo” desinformación, es una fuente clave para investigación de moderación/transparencia relacionada con contenidos (incluyendo desinformación según categorías/decisiones).

### B. **DSA Transparency Database — Research API (Comisión Europea)**
- **Qué es:** API para investigación, con consultas tipo OpenSearch (DSL/SQL) sobre índices (statement_index).
- **Docs:** https://transparency.dsa.ec.europa.eu/page/research-api
- **Base URL:** `https://transparency.dsa.ec.europa.eu/api/v1/research` (ver `evidence/dsa_research_api.html`).
- **Autenticación:** Bearer token requerido (según la documentación; ver `evidence/dsa_research_api.html`).

### C. **EUvsDisinfo (EEAS / East StratCom Task Force)**
- **Qué es:** archivo/catálogo público de casos/narrativas de desinformación (especialmente pro-Kremlin) + contenido editorial.
- **URL:** https://euvsdisinfo.eu/
- **Estado de acceso desde este entorno:** bloqueado por desafío anti-bot (HTTP 403 con “Cf-Mitigated: challenge”; ver `evidence/euvsdisinfo_headers.txt`).
- **Contexto institucional (verificado):** la página del EEAS sobre FIMI enlaza a EUvsDisinfo y afirma que incluye “the world’s largest public archive of pro-Kremlin disinformation” (capturado en `/tmp/fimi2.html`).

### D. **EEAS — Information Integrity & Countering FIMI (Foreign Information Manipulation and Interference)**
- **Qué es:** página marco del EEAS sobre integridad de la información/FIMI; sirve como hub institucional (incluye enlaces a EUvsDisinfo y reportes).
- **URL:** https://www.eeas.europa.eu/eeas/information-integrity-and-countering-foreign-information-manipulation-interference-fimi_en

### E. **Código de Prácticas/Conducta sobre Desinformación (Comisión Europea)**
- **Qué es:** página oficial de política sobre el “2022 Code of Practice on Disinformation”.
- **URL:** https://digital-strategy.ec.europa.eu/en/policies/code-practice-disinformation
- **Evidencia (capturada):** `og:title` “The 2022 Code of Practice on Disinformation” (ver `evidence/ec_code_of_practice.html`).

### F. **DisinfoCode.eu — Transparency Center / Reports (reporting de signatarios del Código)**
- **Qué es:** portal que publica/organiza reportes de transparencia asociados al Código (ahora “Code of Conduct” bajo DSA, según el propio sitio).
- **URLs:**
  - Home: https://disinfocode.eu/
  - Reports: https://disinfocode.eu/reports
- **Exportaciones estructuradas (verificadas):**
  - JSON: `https://disinfocode.eu/reports/{signatory}/{report_id}/json`
  - CSV: `https://disinfocode.eu/reports/{signatory}/{report_id}/csv`
  - Ejemplo descargado: `https://disinfocode.eu/reports/avaaz/8/json` (ver `evidence/disinfocode_avaaz8.json`) y CSV correspondiente (`evidence/disinfocode_avaaz8.csv`).

### G. **EDMO — European Digital Media Observatory (portal paneuropeo)**
- **Qué es:** observatorio paneuropeo (red/hubs) que publica contenidos, recursos y enlaces sobre desinformación.
- **URL:** https://edmo.eu/
- **Nota técnica:** el sitio anuncia WordPress REST API (`/wp-json/`) en headers (ver `evidence/edmo_home.html`). En este entorno, peticiones a endpoints específicos se quedaron sin respuesta (timeout).

### H. **SOMA Disinfobservatory (proyecto/portal de observación)**
- **URL:** https://www.disinfobservatory.org/
- **Nota técnica:** WordPress REST API anunciada en headers (ver `evidence/soma_home.html`).

---

## 2) Estados miembros — ejemplos de fuentes oficiales relevantes

### Suecia — **Myndigheten för psykologiskt försvar (MPF)**
- **Qué es:** agencia sueca orientada a “psicológico/defensa” e integridad del debate público.
- **URL:** https://www.mpf.se/
- **Evidencia (capturada):** título HTML “Myndigheten för psykologiskt försvar” (ver `evidence/mpf_home.html`).

### España — **DSN: “Sistema de lucha contra la desinformación”**
- **URL:** https://www.dsn.gob.es/es/actualidad/sistema-lucha-contra-desinformacion
- **Estado de acceso desde este entorno:** bloqueado por WAF (“Request Denied!”; ver `/tmp/dsn_desinfo.html`).

### Francia — **Viginum**
- **URL:** https://www.viginum.gouv.fr/
- **Estado de acceso desde este entorno:** fallo de conexión/DNS (curl exit code 6); no verificado el contenido.

---

## 3) Fuentes complementarias (incidentes/entorno informativo, no solo desinformación)

### Mapping Media Freedom (MMF)
- **Qué es:** base de incidentes sobre violaciones a la libertad de prensa y de medios en Estados miembros y países candidatos.
- **URL:** https://www.mappingmediafreedom.org/
- **Evidencia (capturada):** meta descripción indica cobertura UE + países candidatos (capturado durante sesión; homepage guardada como `evidence/mmf_home.html`).

---

## Archivos de salida
- Lista estructurada: `eu_disinfo_sources.json`
- Evidencias descargadas: carpeta `evidence/`
- Fichas wiki por fuente: `.openplanter/wiki/*.md` y el índice `.openplanter/wiki/index.md`

## Limitaciones conocidas
- No se pudo usar búsqueda web (EXA_API_KEY no configurada), por lo que la lista está sesgada a fuentes verificadas directamente y algunas muy conocidas.
- Varias webs aplican protecciones anti-bot/WAF que impiden verificación automática completa (p.ej., EUvsDisinfo, DSN España).
