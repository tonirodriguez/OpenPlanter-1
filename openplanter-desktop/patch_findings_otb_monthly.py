import re

PATH = 'findings.md'

# Text to insert in the resumen ejecutivo: between item 8 and item 9 (2027)
INSERT_RESUMEN = "\n9) **Barcelona (abril y mayo 2026, OTB \u201cPerfil del turista a la Destinaci\u00f3 Barcelona\u201d)**: *estada mitjana* (nits) **4,0** (abril 2026) y **4,1** (mayo 2026). *(Confirmado; instant\u00e1neas mensuales)*\n"

# Evidence block to insert after the Barcelona universe section
INSERT_EVIDENCIA = "\n### Barcelona \u2014 OTB (perfil mensual 2026: \u201cPerfil del turista a la Destinaci\u00f3 Barcelona\u201d)\nFuentes:\n\n- `evidence/otb_2604_informe_mensual_perfil_destinacio.pdf.txt`\n  - (l\u00edneas 169\u2013174) bloque \u201c**Perfil del turista a la Destinaci\u00f3 Barcelona \u2014 Abril 2026**\u201d con \u201c**Estada mitjana (nits) 4,0**\u201d y distribuciones de sexo/origen/motivo/canal.\n- `evidence/otb_2605_informe_mensual_perfil_destinacio.pdf.txt`\n  - (l\u00edneas 169\u2013174) bloque \u201c**Perfil del turista a la Destinaci\u00f3 Barcelona \u2014 Maig 2026**\u201d con \u201c**Estada mitjana (nits) 4,1**\u201d y distribuciones de sexo/origen/motivo/canal.\n"


def main():
    raw = open(PATH, 'r', encoding='utf-8', errors='replace').read()

    # 1) Insert resumen item before the current '9) **2027**'
    # Use a tolerant pattern because of possible mojibake in the file.
    m = re.search(r"\n9\) \*\*2027\*\*:", raw)
    if not m:
        raise SystemExit('Could not find 9) **2027** in resumen ejecutivo')

    # Avoid duplicate insertion
    if 'Perfil del turista a la Destinació Barcelona' not in raw:
        raw = raw[:m.start()] + INSERT_RESUMEN + raw[m.start():]
        # Renumber the original 9) 2027 -> 10)
        raw = raw.replace('\n9) **2027**:', '\n10) **2027**:', 1)

    # 2) Insert evidence block after the Barcelona universe section (after its bullet quote)
    if 'perfil mensual 2026' not in raw:
        # Find the Barcelona universe evidence bullet line
        m2 = re.search(r"\n### Barcelona .*\nFuente: `evidence/otb_2025_capsula1_IAOTB_1\.pdf\.txt`\n\n- \(l", raw)
        if not m2:
            # fallback: insert before markets-of-origin header
            m3 = re.search(r"\n## Mercados de origen / emisores", raw)
            if not m3:
                raise SystemExit('Could not locate insertion point for Barcelona evidence block')
            raw = raw[:m3.start()] + INSERT_EVIDENCIA + '\n' + raw[m3.start():]
        else:
            # Insert right after the first Barcelona bullet block (up to the next blank line)
            start = m2.start()
            # Find the blank line following the Barcelona bullet quote
            after = raw.find('\n\n## Mercados de origen', start)
            if after == -1:
                # place at next section header
                after = raw.find('\n## ', start)
            if after == -1:
                after = len(raw)
            raw = raw[:after] + INSERT_EVIDENCIA + raw[after:]

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(raw)


if __name__ == '__main__':
    main()
