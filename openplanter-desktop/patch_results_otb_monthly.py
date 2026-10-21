import json

RESULTS_PATH = 'results.json'


def main():
    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        d = json.load(f)

    # 1) Add OTB monthly profile sources (if missing)
    new_sources = [
        {
            "name": "Observatori del Turisme a Barcelona (OTB)  -  Informe mensual perfil Destinació (Abril 2026) PDF",
            "canonical_url": "https://observatoriturisme.barcelona/wp-content/uploads/2026/05/2604_Informe-mensual-perfil-Destinacio.pdf",
            "local_evidence_files": [
                "evidence/otb_2604_informe_mensual_perfil_destinacio.pdf",
                "evidence/otb_2604_informe_mensual_perfil_destinacio.pdf.txt",
                "_otb_2604_dest_snip.txt"
            ]
        },
        {
            "name": "Observatori del Turisme a Barcelona (OTB)  -  Informe mensual perfil Destinació (Maig 2026) PDF",
            "canonical_url": "https://observatoriturisme.barcelona/wp-content/uploads/2026/06/2605_Informe-mensual-perfil-Destinacio.pdf",
            "local_evidence_files": [
                "evidence/otb_2605_informe_mensual_perfil_destinacio.pdf",
                "evidence/otb_2605_informe_mensual_perfil_destinacio.pdf.txt",
                "_otb_2605_dest_snip.txt"
            ]
        }
    ]

    existing_names = {s.get('name') for s in d.get('sources_used', [])}
    for s in new_sources:
        if s['name'] not in existing_names:
            d.setdefault('sources_used', []).append(s)

    # 2) Add OTB monthly observations (if missing)
    new_obs = [
        {
            "period": "Abril 2026 (Barcelona, OTB - Perfil del turista a la Destinació Barcelona)",
            "statement": "OTB (informe mensual de perfil) muestra para abril 2026, en el bloque “Perfil del turista a la Destinació Barcelona”, una estada mitjana (nits) de 4,0 y distribuciones de sexo/origen/motivo/canal de contratación.",
            "values": {
                "average_stay_nights": "4,0",
                "sex": {"female": "36,4%", "male": "63,6%"},
                "origin": {"catalunya": "16,3%", "resta_d_europa": "15,2%", "resta_d_espanya": "49,1%", "resta_del_mon": "19,5%"},
                "trip_purpose": {"oci": "63,2%", "professional": "19,6%", "personal_i_altres": "17,1%"},
                "booking_channel": {"directe": "44,2%", "ttoo": "43,0%", "altres": "1,9%", "ns_nc": "11,0%"}
            },
            "evidence": {
                "local_file": "evidence/otb_2604_informe_mensual_perfil_destinacio.pdf.txt",
                "line_numbers": [169, 171, 173, 174]
            },
            "confidence": "confirmed (monthly profile snapshot; provisional/unweighted per footnote in PDF)"
        },
        {
            "period": "Maig 2026 (Barcelona, OTB - Perfil del turista a la Destinació Barcelona)",
            "statement": "OTB (informe mensual de perfil) muestra para mayo 2026, en el bloque “Perfil del turista a la Destinació Barcelona”, una estada mitjana (nits) de 4,1 y distribuciones de sexo/origen/motivo/canal de contratación.",
            "values": {
                "average_stay_nights": "4,1",
                "sex": {"female": "34,9%", "male": "65,1%"},
                "origin": {"catalunya": "12,8%", "resta_d_europa": "12,1%", "resta_d_espanya": "51,8%", "resta_del_mon": "23,2%"},
                "trip_purpose": {"oci": "56,4%", "professional": "29,5%", "personal_i_altres": "14,1%"},
                "booking_channel": {"directe": "44,0%", "ttoo": "41,2%", "altres": "1,9%", "ns_nc": "12,8%"}
            },
            "evidence": {
                "local_file": "evidence/otb_2605_informe_mensual_perfil_destinacio.pdf.txt",
                "line_numbers": [169, 171, 173, 174]
            },
            "confidence": "confirmed (monthly profile snapshot; provisional/unweighted per footnote in PDF)"
        }
    ]

    existing_periods = {o.get('period') for o in d.get('observations', [])}
    for o in new_obs:
        if o['period'] not in existing_periods:
            d.setdefault('observations', []).insert(9, o)  # place after 2025 Barcelona universe obs (index 8)
            existing_periods.add(o['period'])

    with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
