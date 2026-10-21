#!/usr/bin/env python3
"""
Search for recent Apple security breaches using web search and direct URL fetching.
"""

import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# Known Apple security breach sources to check
SOURCES = [
    "https://support.apple.com/en-us/HT201222",  # Apple security updates
    "https://www.apple.com/security/",  # Apple security page
    "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",  # CISA KEV
]

# Search queries for known breaches
SEARCH_QUERIES = [
    "Apple security breach 2024",
    "Apple security breach 2025", 
    "Apple data breach 2024",
    "Apple data breach 2025",
    "Apple iCloud breach 2024",
    "Apple iCloud breach 2025",
    "Apple employee credential theft 2024",
    "Apple supplier breach 2024",
    "Apple zero-day 2024",
    "Apple zero-day 2025",
]

def fetch_url(url):
    """Fetch a URL and return content."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"ERROR: {e}"

def search_duckduckgo(query):
    """Search using DuckDuckGo HTML (no API key needed)."""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"ERROR: {e}"

import urllib.parse

def extract_links(html):
    """Extract links from HTML."""
    links = re.findall(r'href=["\']([^"\']+)["\']', html)
    return [l for l in links if l.startswith('http')]

def main():
    results = {
        "search_date": datetime.now().isoformat(),
        "sources_checked": [],
        "potential_breaches": [],
    }
    
    # Check known sources
    for url in SOURCES:
        print(f"Fetching {url}...")
        content = fetch_url(url)
        results["sources_checked"].append({"url": url, "status": "success" if not content.startswith("ERROR") else "error", "length": len(content)})
        
        # Look for breach-related content
        if "breach" in content.lower() or "incident" in content.lower() or "vulnerability" in content.lower():
            results["potential_breaches"].append({
                "source": url,
                "snippet": content[:500]
            })
    
    # Search for breaches
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")
        html = search_duckduckgo(query)
        links = extract_links(html)
        results["potential_breaches"].append({
            "query": query,
            "top_links": links[:10]
        })
    
    with open("apple_breach_search_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to apple_breach_search_results.json")

if __name__ == "__main__":
    main()