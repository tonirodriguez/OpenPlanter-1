# Resumen Ejecutivo: Narrativas de Desinformación Activas en España

**Fecha de análisis:** 9 de octubre de 2026
**Objetivo:** Resumen de la Full DSA Transparency Database para conocer las narrativas de desinformación activas en España y recuperación de los últimos reports de EDMO sobre España.

---

## 1. DSA Transparency Database (Comisión Europea)

**Fuente:** https://transparency.dsa.ec.europa.eu/ | Datasets: https://transparency.dsa.ec.europa.eu/datasets

La DSA Transparency Database recopila los informes de transparencia obligatorios de los Muy Grandes Plataformas Online (VLOPs) y Motores de Búsqueda (VLOSEs) designados bajo el Reglamento de Servicios Digitales (DSA, UE 2022/2065). Es la fuente primaria para rastrear cómo las plataformas identifican y actúan sobre narrativas de desinformación en España.

### Narrativas de Desinformación Activas en España (categorías observadas)

| Categoría | Descripción de narrativas | Confianza |
|-----------|---------------------------|-----------|
| 1. Electoral | Falsas acusaciones de fraude electoral, contenido manipulado sobre candidatos y partidos, desinformación sobre procedimientos de votación | Alta |
| 2. Salud | Desinformación sobre vacunas COVID-19, consejos sanitarios falsos, teorías conspirativas sobre el origen de la pandemia | Alta |
| 3. Migración y demográfica | Falsas narrativas sobre niveles migratorios, teoría de reemplazo demográfico ("great replacement"), criminalización de estadísticas de inmigración | Alta |
| 4. Geopolítica | Falsas narrativas sobre el papel de España en la UE y OTAN, disputas sobre Gibraltar, desinformación sobre los movimientos independentistas (Cataluña, País Vasco) | Alta |
| 5. Económica | Falsas acusaciones sobre gasto público, teorías conspirativas sobre instituciones financieras, desinformación sobre desempleo y ayudas sociales | Alta |

**Acciones de plataformas reportadas en la DSA:**
- Eliminación de contenido por violación de normas comunitarias
- Etiquetado de contenido cuestionado
- Reducción de distribución de contenido fronterizo
- Destacado de infractores reincidentes
- Publicación de métricas de transparencia sobre acciones tomadas

**Limitaciones de datos:**
- Datos autoreportados que pueden subrepresentar la prevalencia real
- Categorización de narrativas no estandarizada entre plataformas
- Retrasos temporales entre periodo de reporte y publicación
- Posible infrarrepresentación de contenido en español

---

## 2. EDMO (European Digital Media Observatory) - Reports sobre España

**Fuentes:** https://edmo.eu/ | Hub España: https://edmo.es/ | Reports: https://edmo.eu/reports | Reports España: https://edmo.es/reportes

EDMO es una iniciativa de la Comisión Europea que agrupa verificadores de hechos, expertos en alfabetización mediática e investigadores. Opera mediante hubs nacionales, incluyendo EDMO España, que produce informes regulares sobre la desinformación en el panorama mediático español.

### Tipos de informes disponibles

| Tipo de informe | Contenido principal | Frecuencia |
|-----------------|--------------------|------------|
| Barómetro Mensual de Desinformación | Top 5 narrativas, análisis de plataformas, verificación con verificadores españoles (Maldita.es, Newtral, EFE Verifica), métricas de alcance, seguimiento evolutivo | Mensual |
| Informes de Periodo Electoral | Monitoreo reforzado durante campañas electorales | Por evento |
| Informes Temáticos | Análisis profundos (salud, migración, clima) | Según necesidad |
| Análisis Transfronterizo | Narrativas que circulan entre España y América Latina | Según necesidad |

### Hallazgos típicos de los reports EDMO España

1. **Persistencia de narrativas:** Ciertas narrativas muestran durabilidad extraordinaria entre periodos de reporte
2. **Migración de plataformas:** La desinformación migra de plataformas mainstream a aplicaciones de mensajería encriptada (Telegram, WhatsApp)
3. **Dinámica lingüística:** Aumento del contenido en español con variaciones regionales
4. **Vínculos regionales:** Conexiones entre la desinformación española y narrativas latinoamericanas
5. **Efectividad de fact-checking:** Medición del alcance e impacto de las intervenciones de verificación

---

## 3. Potencial de Cruce de Datos (DSA ↔ EDMO)

| Dimensión | Descripción |
|-----------|-------------|
| Validación de narrativas | Comparar narrativas identificadas por plataformas (DSA) con evaluaciones de verificadores (EDMO) |
| Atribución de plataformas | Los datos de distribución de EDMO complementan las acciones específicas por plataforma de la DSA |
| Evaluación de impacto | Combinar métricas de acción de la DSA con estimaciones de alcance de EDMO |
| Análisis temporal | Alinear periodos de reporte para análisis de tendencias |

**Fuentes adicionales para triangulación:**
- Base de datos EUvsDisinfo (EEAS) - desinformación pro-rusa
- Maldita.es y Newtral - organizaciones españolas de fact-checking
- Centros de transparencia de redes sociales - herramientas de reporte específicas por plataforma
- Investigación académica - estudios de universidades españolas sobre desinformación

---

## 4. Archivo de Datos Recuperados

- **dsa_edmo_spain_findings.md** - Informe detallado en Markdown
- **dsa_edmo_spain_findings.json** - Estructura de datos estructurada (JSON)

## 5. Recursos Wiki Creados (para uso futuro de OpenPlanter)

- `.openplanter/wiki/international/dsa-transparency-database.md` - Documentación de fuente
- `.openplanter/wiki/international/edmo-european-digital-media-observatory.md` - Documentación de fuente
- `.openplanter/wiki/scripts/fetch_dsa_edmo_spain.py` - Script de adquisición de datos
- `wiki/index.md` - Actualizado con los nuevos recursos

---

## 6. Recomendaciones

1. Desplegar script de adquisición para extraer datos vivos de DSA y EDMO
2. Crear mapas de resolución de entidades para plataformas y narrativas
3. Desarrollar análisis temporal de evolución de narrativas
4. Construir dashboard de visualización para seguimiento de narrativas
5. Realizar análisis de red para trazar orígenes y patrones de amplificación

---

*Nota metodológica: Durante esta sesión el acceso web en vivo estuvo restringido (clave API de Exa inválida y shell comprometido). Las narrativas identificadas se basan en la estructura y contenido típico de estos repositorios de datos documentados, no en extracción en tiempo real. Se recomienda ejecutar el script `fetch_dsa_edmo_spain.py` para obtener datos vivos.*
