import json

# Update findings/results in-place for Spain (INE FRONTUR/EGATUR) and Barcelona (OTB capsule)
# Avoid external deps; use basic file ops.

FINDINGS_PATH = 'findings.md'
RESULTS_PATH = 'results.json'


def insert_after_heading(lines, heading, new_block):
    for i, line in enumerate(lines):
        if line.strip() == heading:
            # insert after heading line
            return lines[: i + 1] + ['\n'] + new_block.splitlines(True) + ['\n'] + lines[i + 1 :]
    raise ValueError(f'Heading not found: {heading}')


def replace_title(lines, old, new):
    for i, line in enumerate(lines):
        if line.strip() == old:
            lines[i] = new + '\n'
            return lines
    raise ValueError('Old title not found')


def update_resumen_ejecutivo(lines, additional_items):
    # Find block starting at '## Resumen ejecutivo' and insert items before the '## Evidencias clave (citas)' heading
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == '## Resumen ejecutivo':
            start = i
        if start is not None and i > start and line.strip() == '## Evidencias clave (citas)':
            end = i
            break
    if start is None or end is None:
        raise ValueError('Could not locate Resumen ejecutivo block')

    # Replace the intro line to include additional sources if present
    # Keep existing line but broaden it.
    for j in range(start, end):
        if lines[j].startswith('Con evidencia de'):
            lines[j] = 'Con evidencia de **UN Tourism (antes UNWTO)**, **INE (España) FRONTUR/EGATUR** y **Observatori del Turisme a Barcelona (OTB)**:\n'
            break

    # Insert new items after existing item 3 (or at end of list if not found)
    insert_at = None
    for j in range(start, end):
        if lines[j].lstrip().startswith('3) '):
            # find next blank line after item 3 block
            k = j
            while k < end and lines[k].strip() != '':
                k += 1
            # skip following blank(s)
            while k < end and lines[k].strip() == '':
                k += 1
            insert_at = k
            break
    if insert_at is None:
        insert_at = end

    # Remove old item 4 about 2027 so we can append updated numbering
    # We'll delete any line starting with '4) **2027**' in resumen block.
    new_resumen = []
    for j in range(start, end):
        if lines[j].lstrip().startswith('4) **2027**'):
            # skip this paragraph (until next blank line)
            k = j
            while k < end and lines[k].strip() != '':
                k += 1
            # also skip subsequent blank lines
            while k < end and lines[k].strip() == '':
                k += 1
            # copy rest later
            new_resumen.extend(lines[start:j])
            new_resumen.extend(lines[k:end])
            lines = lines[:start] + new_resumen + lines[end:]
            # recompute end index by searching again
            return update_resumen_ejecutivo(lines, additional_items)

    # If no old 2027 line, proceed inserting new items at insert_at
    lines = lines[:insert_at] + [l + ('\n' if not l.endswith('\n') else '') for l in additional_items] + ['\n'] + lines[insert_at:]

    # Add updated 2027 statement as last item with correct numbering (after appended items)
    # Determine next number by scanning existing items in resumen
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == '## Resumen ejecutivo':
            start = i
        if start is not None and i > start and line.strip() == '## Evidencias clave (citas)':
            end = i
            break
    nums = []
    for j in range(start, end):
        s = lines[j].lstrip()
        if len(s) >= 3 and s[0].isdigit() and s[1] == ')' and s[2] == ' ':
            try:
                nums.append(int(s.split(')')[0]))
            except Exception:
                pass
    next_n = (max(nums) + 1) if nums else 4
    statement_2027 = f"{next_n}) **2027**: en las fuentes accedidas aquí **no aparece una previsión cuantitativa explícita** (ni global, ni España, ni Barcelona) para 2027. El extracto del barómetro aporta **contexto macro** (IMF/UNDESA) con crecimiento del PIB mundial proyectado para 2027, pero **no traduce** eso a una cifra de turismo. *(Ausencia de evidencia cuantitativa en estas fuentes)*"

    # Insert before end
    lines = lines[:end] + [statement_2027 + '\n', '\n'] + lines[end:]
    return lines


def add_evidencias(lines, block):
    # Insert block before '## Lectura analítica (2026 vs 2025)'
    heading = '## Lectura analítica (2026 vs 2025)'
    for i, line in enumerate(lines):
        if line.strip() == heading:
            return lines[:i] + block.splitlines(True) + ['\n'] + lines[i:]
    raise ValueError('Could not find analysis heading')


def add_sections_before_methodology(lines, block):
    # Insert block before '## Metodología (proveniencia)'
    heading = '## Metodología (proveniencia)'
    for i, line in enumerate(lines):
        if line.strip() == heading:
            return lines[:i] + block.splitlines(True) + ['\n'] + lines[i:]
    raise ValueError('Could not find methodology heading')


def update_methodology(lines, additions):
    # Insert additions as new numbered items after existing methodology items
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == '## Metodología (proveniencia)':
            start = i
            continue
        if start is not None and i > start and line.strip().startswith('## '):
            end = i
            break
    if start is None:
        raise ValueError('No methodology heading')
    if end is None:
        end = len(lines)

    # find last numbered item line within block
    last_num = 0
    last_idx = start
    for j in range(start, end):
        s = lines[j].strip()
        if len(s) >= 3 and s[0].isdigit() and s[1] == ')' and s[2] == ' ':
            try:
                last_num = max(last_num, int(s.split(')')[0]))
                last_idx = j
            except Exception:
                pass

    insert_at = end
    # insert before end but after current list
    new_items = []
    for k, text in enumerate(additions, start=last_num + 1):
        new_items.append(f"{k}) {text}\n")
    return lines[:insert_at] + new_items + ['\n'] + lines[insert_at:]


def update_limitations(lines, extra_bullets):
    # Append extra bullets to Limitaciones section
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == '## Limitaciones':
            start = i
            continue
        if start is not None and i > start and line.strip().startswith('#'):
            end = i
            break
    if start is None:
        raise ValueError('No Limitaciones heading')
    if end is None:
        end = len(lines)

    # insert before end
    bullets = [f"- {b}\n" for b in extra_bullets]
    return lines[:end] + bullets


# ---- Update findings.md ----
with open(FINDINGS_PATH, 'r', encoding='utf-8') as f:
    flines = f.readlines()

flines = replace_title(flines,
                       '# Tendencias de turismo internacional: 2026 vs 2025 y qué se esperaba para 2027',
                       '# Tendencias de turismo internacional (global) y evolución 2025/2026 para España y Barcelona; expectativas 2027')

resumen_items = [
    '4) **España (2025, FRONTUR)**: **96,8 millones** de turistas internacionales en 2025 (**+3,2%** vs 2024; nuevo máximo histórico). *(Confirmado)*',
    '5) **España (ene–jul 2026, FRONTUR)**: en los **siete primeros meses de 2026** el número de turistas **aumentó 4,6%** y **superó los 58,1 millones**. *(Confirmado)*',
    '6) **España (2025, EGATUR)**: gasto total de turistas internacionales **134.712 millones de euros** en 2025 (**+6,8%** vs 2024). *(Confirmado)*',
    '7) **España (ene–jul 2026, EGATUR)**: gasto total **82.054 millones de euros** en los **siete primeros meses de 2026** (**+7,8%** vs mismo periodo 2025). *(Confirmado)*',
    '8) **Barcelona (2025, OTB “Càpsula” IAOTB)**: universo de turistas 2025: **Barcelona ciudad 16,0M**, **Barcelona región 10,1M**, **Destinació Barcelona 26,1M**. *(Confirmado)*',
]
flines = update_resumen_ejecutivo(flines, resumen_items)

new_evid_block = (
"### España — FRONTUR (turistas internacionales)\n"
"Fuentes:\n\n"
"- `evidence/ine_FRONTUR1225.html`\n"
"  - (línea 963) “**Durante el año 2025 visitaron España 96,8 millones de turistas, lo que supuso un nuevo máximo histórico y un aumento del 3,2% respecto al año anterior.**”\n"
"- `evidence/ine_FRONTUR0726.html`\n"
"  - (línea 380) “**En los siete primeros meses de 2026 el número de turistas que visitaron España aumentó un 4,6% y superó los 58,1 millones.**”\n\n"
"### España — EGATUR (gasto total)\n"
"Fuentes:\n\n"
"- `evidence/ine_EGATUR1225.html`\n"
"  - (línea 1103) “**El gasto total realizado por los turistas no residentes en España durante el año 2025 fue de 134.712 millones de euros, lo que supuso un aumento del 6,8% respecto al de 2024.**”\n"
"- `evidence/ine_EGATUR0726.html`\n"
"  - (línea 456) “**Durante los siete primeros meses de 2026 el gasto total de los turistas internacionales aumentó un 7,8% y alcanzó los 82.054 millones de euros.**”\n\n"
"### Barcelona — OTB (universo de turistas)\n"
"Fuente: `evidence/otb_2025_capsula1_IAOTB_1.pdf.txt`\n\n"
"- (líneas 136–138) “**...durant el 2025... 16,0M... sumats als 10,1M... la Destinació Barcelona... 26,1M.**”\n"
)
flines = add_evidencias(flines, new_evid_block)

spain_block = (
"## España (INE): lectura 2025 vs 2026 (YTD)\n\n"
"- **Volumen (FRONTUR)**: 2025 cerró con **96,8M** turistas (+3,2% vs 2024). En **ene–jul 2026**, el acumulado “supera 58,1M” y crece **+4,6%** vs ene–jul 2025.\n"
"- **Valor (EGATUR)**: 2025 cerró con **134.712M€** (+6,8% vs 2024). En **ene–jul 2026**, el gasto acumulado **82.054M€** crece **+7,8%** vs ene–jul 2025.\n\n"
"Nota: las cifras de 2026 citadas aquí son **acumulado de 7 meses**, por lo que no se comparan directamente con el total anual 2025.\n\n"
"## Barcelona (OTB): lectura 2025 y encaje con España\n\n"
"- El OTB reporta para 2025 un **universo de turistas** de **16,0M** (Barcelona ciudad) + **10,1M** (Barcelona región) = **26,1M** (Destinació Barcelona). Esta métrica no es idéntica a FRONTUR (turistas internacionales), por lo que se usa como **indicador local** y no como subconjunto directo de FRONTUR.\n"
)
flines = add_sections_before_methodology(flines, spain_block)

flines = update_methodology(
    flines,
    [
        'Para INE (FRONTUR/EGATUR), se capturaron páginas HTML concretas y se citan las frases con cifras y periodos.',
        'Para OTB, se descargó el PDF “Càpsula” y se extrajo texto con `pdftotext -layout`.',
    ],
)

flines = update_limitations(
    flines,
    [
        'Barcelona: la métrica OTB (“universo de turistas” para Destinació Barcelona) no es estrictamente comparable con FRONTUR (turistas internacionales). Sin una definición metodológica completa en el propio PDF, se reporta con cautela y como indicador local.',
    ],
)

with open(FINDINGS_PATH, 'w', encoding='utf-8') as f:
    f.writelines(flines)


# ---- Update results.json ----
with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
    results = json.load(f)

# Ensure sources list includes INE/OTB
sources = results.get('sources_used', [])

# helper to avoid duplicates by canonical_url or name

def has_source(name=None, canonical_url=None):
    for s in sources:
        if canonical_url and s.get('canonical_url') == canonical_url:
            return True
        if name and s.get('name') == name:
            return True
    return False

if not has_source(name='INE (España) — FRONTUR (Nota de Prensa) HTML'):
    sources.append({
        'name': 'INE (España) — FRONTUR (Nota de Prensa) HTML',
        'canonical_url': 'https://www.ine.es/dyngs/Prensa/FRONTUR1225.htm',
        'local_evidence_files': [
            'evidence/ine_FRONTUR1225.html',
            'evidence/ine_FRONTUR0726.html'
        ]
    })

if not has_source(name='INE (España) — EGATUR (Nota de Prensa) HTML'):
    sources.append({
        'name': 'INE (España) — EGATUR (Nota de Prensa) HTML',
        'canonical_url': 'https://www.ine.es/dyngs/Prensa/EGATUR1225.htm',
        'local_evidence_files': [
            'evidence/ine_EGATUR1225.html',
            'evidence/ine_EGATUR0726.html'
        ]
    })

if not has_source(name='Observatori del Turisme a Barcelona (OTB) — IAOTB Càpsula PDF (2025)'):
    sources.append({
        'name': 'Observatori del Turisme a Barcelona (OTB) — IAOTB Càpsula PDF (2025)',
        'canonical_url': 'https://observatoriturisme.barcelona/wp-content/uploads/2026/02/2025_Capsula-1-IAOTB-1.pdf',
        'local_evidence_files': [
            'evidence/otb_2025_capsula1_IAOTB_1.pdf',
            'evidence/otb_2025_capsula1_IAOTB_1.pdf.txt'
        ]
    })

results['sources_used'] = sources

obs = results.get('observations', [])

# Append observations (do not delete existing global ones)
obs.extend([
    {
        'period': '2025 (España, FRONTUR full year)',
        'statement': 'Durante el año 2025 visitaron España 96,8 millones de turistas; nuevo máximo histórico; +3,2% vs 2024.',
        'values': {
            'tourists_international_millions': '96,8 millones',
            'yoy_growth_percent': '3,2%'
        },
        'evidence': {
            'local_file': 'evidence/ine_FRONTUR1225.html',
            'line_numbers': [963],
            'also_present_as_embedded_numeric_string': '96.770.515'
        },
        'confidence': 'confirmed'
    },
    {
        'period': 'Ene–Jul 2026 vs Ene–Jul 2025 (España, FRONTUR)',
        'statement': 'En los siete primeros meses de 2026 el número de turistas aumentó un 4,6% y superó los 58,1 millones.',
        'values': {
            'tourists_international': 'superó los 58,1 millones',
            'yoy_growth_percent': '4,6%'
        },
        'evidence': {
            'local_file': 'evidence/ine_FRONTUR0726.html',
            'line_numbers': [380],
            'embedded_numeric_string': '58.106.406'
        },
        'confidence': 'confirmed'
    },
    {
        'period': '2025 (España, EGATUR full year)',
        'statement': 'El gasto total de turistas internacionales en 2025 fue de 134.712 millones de euros; +6,8% vs 2024.',
        'values': {
            'spend_total_million_eur': '134.712',
            'yoy_growth_percent': '6,8%'
        },
        'evidence': {
            'local_file': 'evidence/ine_EGATUR1225.html',
            'line_numbers': [1103]
        },
        'confidence': 'confirmed'
    },
    {
        'period': 'Ene–Jul 2026 vs Ene–Jul 2025 (España, EGATUR)',
        'statement': 'Durante los siete primeros meses de 2026 el gasto total aumentó un 7,8% y alcanzó los 82.054 millones de euros.',
        'values': {
            'spend_total_million_eur': '82.054',
            'yoy_growth_percent': '7,8%'
        },
        'evidence': {
            'local_file': 'evidence/ine_EGATUR0726.html',
            'line_numbers': [456]
        },
        'confidence': 'confirmed'
    },
    {
        'period': '2025 (Barcelona, OTB universe of tourists)',
        'statement': 'OTB reporta en 2025: Barcelona ciudad 16,0M de turistas; Barcelona región 10,1M; Destinació Barcelona 26,1M.',
        'values': {
            'barcelona_city_tourists': '16,0M',
            'barcelona_region_tourists': '10,1M',
            'destination_barcelona_tourists': '26,1M'
        },
        'evidence': {
            'local_file': 'evidence/otb_2025_capsula1_IAOTB_1.pdf.txt',
            'line_numbers': [136, 137, 138]
        },
        'confidence': 'confirmed'
    }
])

results['observations'] = obs

# Update methodology note (keep existing, append)
method = results.get('methodology', {})
approach = method.get('approach', '')
extra = ' Added INE FRONTUR/EGATUR press release HTML captures and OTB capsule PDF text extraction (pdftotext -layout) for Spain/Barcelona segmentation.'
method['approach'] = (approach + extra).strip()
results['methodology'] = method

# Update limitations
lims = results.get('limitations', [])
if 'Barcelona OTB metrics are not directly comparable to INE FRONTUR international-arrivals totals (different universe/definition).' not in lims:
    lims.append('Barcelona OTB metrics are not directly comparable to INE FRONTUR international-arrivals totals (different universe/definition).')
results['limitations'] = lims

with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
