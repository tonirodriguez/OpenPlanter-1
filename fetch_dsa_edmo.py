import urllib.request
import urllib.error
import re
import sys

def fetch_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def extract_dsa_narratives(html):
    # Look for disinformation narratives in Spain
    # This is a placeholder; we'll look for common patterns
    narratives = []
    # Look for sections that might contain narratives
    # We'll search for Spanish language and disinformation terms
    spanish_section = re.findall(r'<[^>]*>[^<]*España[^<]*</[^>]*>', html, re.IGNORECASE)
    disinfo_section = re.findall(r'<[^>]*>[^<]*desinformaci[^<]*</[^>]*>', html, re.IGNORECASE)
    # Combine and clean
    for section in spanish_section + disinfo_section:
        # Remove tags and extra whitespace
        text = re.sub('<[^>]+>', '', section)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 20:
            narratives.append(text)
    return narratives[:10]  # Return top 10

def extract_edmo_reports(html):
    # Look for EDMO reports on Spain
    reports = []
    # Look for links or titles that mention Spain and report
    spain_reports = re.findall(r'<[^>]*>[^<]*España[^<]*report[^<]*</[^>]*>', html, re.IGNORECASE)
    spain_reports += re.findall(r'<[^>]*>[^<]*report[^<]*España[^<]*</[^>]*>', html, re.IGNORECASE)
    for report in spain_reports:
        text = re.sub('<[^>]+>', '', report)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 20:
            reports.append(text)
    return reports[:10]

def main():
    dsa_url = "https://transparency.dsa.ec.europa.eu/datasets"
    edmo_url = "https://edmo.eu"
    
    print("Fetching DSA Transparency Database...")
    dsa_html = fetch_url(dsa_url)
    if dsa_html:
        print(f"Fetched DSA page, length: {len(dsa_html)}")
        narratives = extract_dsa_narratives(dsa_html)
        print(f"Found {len(narratives)} potential narratives about Spain")
        with open('/tmp/dsa_narratives.txt', 'w', encoding='utf-8') as f:
            for n in narratives:
                f.write(n + '\n')
    else:
        print("Failed to fetch DSA page")
    
    print("Fetching EDMO website...")
    edmo_html = fetch_url(edmo_url)
    if edmo_html:
        print(f"Fetched EDMO page, length: {len(edmo_html)}")
        reports = extract_edmo_reports(edmo_html)
        print(f"Found {len(reports)} potential reports about Spain")
        with open('/tmp/edmo_reports.txt', 'w', encoding='utf-8') as f:
            for r in reports:
                f.write(r + '\n')
    else:
        print("Failed to fetch EDMO page")

if __name__ == '__main__':
    main()