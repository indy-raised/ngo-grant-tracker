import requests
import pandas as pd
from datetime import datetime

SEARCH_TERMS = [
    "ukraine cultural",
    "cultural heritage preservation",
    "eastern europe arts",
    "arts human rights",
    "museum digital preservation",
    "youth activism arts"
]

BASE_URL = "https://projects.propublica.org/nonprofits/api/v2/search.json"

def fetch_foundations(query):
    params = {"q": query, "ntee[0]": "A"}  # NTEE A = Arts & Culture orgs
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("organizations", [])
    except Exception as e:
        print(f"Error fetching '{query}': {e}")
        return []

def parse_org(org):
    return {
        "funder":         org.get("name", ""),
        "ein":            org.get("ein", ""),
        "city":           org.get("city", ""),
        "state":          org.get("state", ""),
        "ntee_code":      org.get("ntee_code", ""),
        "revenue":        org.get("revenue_amount", ""),
        "assets":         org.get("asset_amount", ""),
        "propublica_url": f"https://projects.propublica.org/nonprofits/organizations/{org.get('ein', '')}",
        "source":         "ProPublica 990",
        "date_pulled":    datetime.today().strftime("%Y-%m-%d")
    }

all_orgs = []
seen_eins = set()

for term in SEARCH_TERMS:
    print(f"Searching foundations: {term}")
    orgs = fetch_foundations(term)
    for org in orgs:
        ein = org.get("ein")
        if ein and ein not in seen_eins:
            seen_eins.add(ein)
            all_orgs.append(parse_org(org))

df = pd.DataFrame(all_orgs)
df.to_csv("foundations_raw.csv", index=False)
print(f"Saved {len(df)} foundations from ProPublica")
