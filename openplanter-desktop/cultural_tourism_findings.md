# Datos cuantitativos disponibles sobre “turismo cultural” (España vs Barcelona) — evidencias en el workspace

## Resumen (qué hay y qué no hay)

- **Barcelona (sí hay indicador cuantitativo relacionado con cultura)**: en los PDFs mensuales del **Observatori del Turisme a Barcelona (OTB)** aparece el indicador de actividades realizadas, incluyendo **“Visites culturals”** (respuesta múltiple) con porcentajes para **Barcelona Ciutat / Barcelona Regió / Destinació Barcelona** (abril 2026 y mayo 2026). *(Confirmado en capturas locales)*

- **España (en estas capturas no hay desglose “cultural” en turismo internacional)**: en las notas de prensa HTML capturadas de **INE FRONTUR/EGATUR** hay totales de turistas y gasto, pero **no se encontró segmentación específica por “turismo cultural”** (motivo/actividad cultural) en esos HTML concretos. *(Ausencia en estas capturas; no prueba ausencia en otras fuentes oficiales)*

- **España (contexto cultural cuantitativo, no turismo)**: sí hay datos cuantitativos sobre el **ecosistema/consumo cultural** (p. ej., visitas a museos en la población, visitantes de museos, gasto público cultural), que pueden usarse como **contexto** pero **no equivalen** a un conteo de “turistas culturales”.

---

## Barcelona: indicador directo (OTB) — “Visites culturals”

### Abril 2026 (OTB)
Fuente: `evidence/otb_2604_informe_mensual_perfil_destinacio.pdf.txt`

En el bloque **“Activitats realitzades al municipi (Resposta múltiple)”**:

- **Barcelona Ciutat**: “Visites culturals” **79,8%** (línea **82**)
- **Barcelona Regió**: “Visites culturals” **50,2%** (línea **145**)
- **Destinació Barcelona**: “Visites culturals” **63,0%** (línea **207**)

### Mayo 2026 (OTB)
Fuente: `evidence/otb_2605_informe_mensual_perfil_destinacio.pdf.txt`

- **Barcelona Ciutat**: “Visites culturals” **76,0%** (línea **75**)
- **Barcelona Regió**: “Visites culturals” **47,1%** (línea **144**)
- **Destinació Barcelona**: “Visites culturals” **59,3%** (línea **208**)

**Interpretación mínima**: es un indicador de **actividad declarada** (respuesta múltiple) dentro del perfil mensual. No es un “motivo principal del viaje” ni un total de llegadas.

---

## España: no aparece “turismo cultural” en las capturas INE (FRONTUR/EGATUR)

- FRONTUR (llegadas totales): `evidence/ine_FRONTUR1225.html`
- EGATUR (gasto total): `evidence/ine_EGATUR1225.html`

En estas capturas se recogen totales anuales (2025) y no se identificó un bloque/tabla de **segmentación cultural**.

---

## España: contexto cuantitativo cultural (no turismo)

### Encuesta de Hábitos y Prácticas Culturales 2024-2025 (Ministerio de Cultura) — visitas declaradas
Fuente: `evidence/02011.xlsx` (exportación de CulturaJaxiPx)

Tabla: “Personas según la asistencia o visita …” (unidades: **En % del total de cada colectivo**; periodo **2024-2025**)

Fila **TOTAL** / “Total han visitado en el último año”:

- **Museos**: **40.6** (celdas `B7/B8/B9/B10`)
- **Exposiciones**: **33.9** (celdas `G7/G8/G9/G10`)
- **Galerías de arte**: **18.5** (celdas `L7/L8/L9/L10`)

### Estadística de Museos y Colecciones Museográficas — visitantes estimados
Fuente: `evidence/T11P1010.csv_sc`

- **TOTAL visitantes 2024**: **63.980.526** (línea **8**, columna 2024)

### Gasto público en cultura (Administración General del Estado) — liquidado
Fuente: `evidence/T301001.csv_sc`

- **Administración General del Estado — TOTAL (en miles de euros), 2024**: **1.248.497** (línea **9**, columna 2024)

### Eurostat (COFOG GF08: Recreation, culture and religion) — España

- `evidence/eurostat_gf08_pc_gdp_es_alltime.json`: **% del PIB** (PC_GDP), España, GF08.
  - **2024: 1.2**
- `evidence/eurostat_gf08_pc_tot_es_2023.json`: **% del gasto total** (PC_TOT), España, GF08.
  - **2023: 2.7**

---

## Metodología (resumen)

1) Se usaron únicamente ficheros en `evidence/` ya capturados.
2) OTB: extracción por búsqueda de las líneas donde aparece “Visites culturals” dentro del bloque “Activitats realitzades al municipi”.
3) EHPC (02011.xlsx): lectura del XML interno (`xl/worksheets/sheet1.xml`) para recuperar encabezados y la fila TOTAL.
4) CSV_SC (T11P1010 / T301001): lectura directa de valores en la fila TOTAL/Administración General del Estado.
5) Eurostat: parseo del JSON de la API de diseminación (dimensión tiempo → valores).

## Limitaciones

- Barcelona: el indicador OTB es porcentual y depende del diseño muestral del informe mensual; es **actividad**, no un “turista cultural” definido por motivo principal.
- España: las notas de prensa FRONTUR/EGATUR usadas aquí no contienen desglose cultural; podrían existir otras tablas/operaciones no consultadas en este paso.
- Los datos de EHPC mostrados son participación cultural de población (contexto), no turismo.

---

## Archivos de salida

- `tourism_cultural_quant_spain_barcelona.json` (resumen inicial, actualizado con segmentos y EHPC)
- `cultural_tourism_metrics_spain_barcelona.json` (métricas estructuradas + metodología + limitaciones)
- `cultural_tourism_findings.md` (este informe)
