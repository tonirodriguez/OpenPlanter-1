import csv, json, re
from pathlib import Path


def read_semicolon_csv(path: Path):
    # Return list of rows (each row list of strings) from a UTF-8 BOM / CRLF file
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    # Normalize newlines for csv
    lines = text.splitlines()
    reader = csv.reader(lines, delimiter=';')
    return [row for row in reader]


def extract_two_block_year_map(rows, year_first):
    """Find header row whose second cell equals year_first, then map first and second block.

    Returns (years, split_index)
    """
    header_idx = None
    years = None
    for i, row in enumerate(rows):
        if len(row) >= 2 and row[1].strip() == str(year_first):
            header_idx = i
            years = [c.strip() for c in row[1:] if c is not None]
            break
    if header_idx is None:
        raise ValueError(f"Could not find year header starting with {year_first}")

    # Find the second occurrence of year_first to split blocks.
    # years corresponds to row[1:], so split index is in years list.
    occurrences = [i for i, y in enumerate(years) if y == str(year_first)]
    if len(occurrences) < 2:
        raise ValueError(f"Could not find second occurrence of {year_first} in year header")
    split = occurrences[1]
    return header_idx, years, split


def parse_t11_museum_visitors(path: Path):
    rows = read_semicolon_csv(path)
    header_idx, years, split = extract_two_block_year_map(rows, 2024)

    # Find TOTAL row (first cell == 'TOTAL') after header
    total_row = None
    for row in rows[header_idx+1:]:
        if len(row) > 0 and row[0].strip() == 'TOTAL':
            total_row = row
            break
    if total_row is None:
        raise ValueError('Could not find TOTAL row')

    values = [c.strip() for c in total_row[1:]]
    block1_years = years[:split]
    block2_years = years[split:]

    block1_vals = values[:split]
    block2_vals = values[split:split+len(block2_years)]

    total_visitors = dict(zip(block1_years, block1_vals))
    per_museum = dict(zip(block2_years, block2_vals))

    # Drop empty year key if present (artifact of trailing delimiter)
    if '' in per_museum:
        per_museum.pop('')

    return {
        'total_visitors': total_visitors,
        'per_museum_or_collection': per_museum,
        'year_header_row_index_1based': header_idx + 1,
    }


def parse_t301_public_culture_spend(path: Path):
    rows = read_semicolon_csv(path)
    header_idx, years, split = extract_two_block_year_map(rows, 2025)

    # We will parse Administración General del Estado section's rows.
    # Identify section start row where first cell == 'Administración General del Estado;'
    section_start = None
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0].strip().startswith('Administración General del Estado'):
            section_start = i
            break
    if section_start is None:
        raise ValueError('Could not find Administración General del Estado section')

    # Row labels we want inside the section
    wanted_prefixes = [
        '    TOTAL (En miles de euros)',
        '    En % del gasto liquidado total',
        '    En % del P.I.B.',
        '    Valores medios por habitante (Euros)',
    ]

    extracted = {}
    for row in rows[section_start:]:
        if len(row) == 0:
            continue
        label = row[0]
        # stop when we reach next major section
        if label.strip().startswith('Administración Autonómica'):
            break
        for pref in wanted_prefixes:
            if label.startswith(pref):
                vals = [c.strip() for c in row[1:]]
                block1_years = years[:split]
                block1_vals = vals[:split]
                extracted[pref.strip()] = dict(zip(block1_years, block1_vals))
                break

    if not extracted:
        raise ValueError('Did not extract any wanted rows in AGE section')

    return {
        'age_section_start_row_index_1based': section_start + 1,
        'year_header_row_index_1based': header_idx + 1,
        'age': extracted,
    }


def parse_eurostat_gf08_pc_gdp_alltime(path: Path):
    d = json.loads(path.read_text(encoding='utf-8', errors='replace'))
    idx = d['dimension']['time']['category']['index']
    inv = {v: k for k, v in idx.items()}
    pairs = []
    for k, v in d.get('value', {}).items():
        pairs.append((inv[int(k)], v))
    return dict(sorted(pairs))


def main():
    out = {}

    out['museums_t11p1010'] = parse_t11_museum_visitors(Path('evidence/T11P1010.csv_sc'))
    out['public_spend_t301001'] = parse_t301_public_culture_spend(Path('evidence/T301001.csv_sc'))
    out['eurostat_gf08_pc_gdp'] = parse_eurostat_gf08_pc_gdp_alltime(Path('evidence/eurostat_gf08_pc_gdp_es_alltime.json'))

    Path('cultural_data_extract.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
