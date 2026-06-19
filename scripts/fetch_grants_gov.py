import requests
import pandas as pd
from datetime import datetime

KEYWORDS = [
    "culture", "cultural preservation", "heritage", "arts",
    "Ukraine", "Eastern Europe", "displacement", "refugees",
    "youth", "activism", "museum", "digital preservation",
    "human rights", "war", "conflict"
]

BASE_URL = "https://apply07.grants.gov/grantsws/rest/opportunities/search/"

def fetch_grants(keyword, rows=25):
    payload = {
        "keyword": keyword,
        "oppStatuses": "forecasted|posted",
        "rows": rows,
        "startRecordNum": 0
    }
    try:
        response = requests.post(BASE_URL, json=payload, timeout=15)
        response.raise_for_status()
        return response.json().get("oppHits", [])
    except Exception as e:
        print(f"Error fetching '{keyword}': {e}")
        return []

def parse_grant(hit):
    return {
        "grant_id":           hit.get("id", ""),
        "funder":             hit.get("agencyName", ""),
        "program":            hit.get("title", ""),
        "opportunity_number": hit.get("number", ""),
        "award_floor":        hit.get("awardFloor", ""),
        "award_ceiling":      hit.get("awardCeiling", ""),
        "deadline":           hit.get("closeDate", ""),
        "post_date":          hit.get("openDate", ""),
        "description":        (hit.get("synopsis", "") or "")[:300],
        "url":                f"https://www.grants.gov/search-results-detail/{hit.get('id', '')}",
        "source":             "Grants.gov",
        "date_pulled":        datetime.today().strftime("%Y-%m-%d")
    }

all_grants = []
seen_ids = set()

for keyword in KEYWORDS:
    print(f"Fetching: {keyword}")
    hits = fetch_grants(keyword)
    for hit in hits:
        gid = hit.get("id")
        if gid and gid not in seen_ids:
            seen_ids.add(gid)
            all_grants.append(parse_grant(hit))

df = pd.DataFrame(all_grants)
df.to_csv("grants_gov_raw.csv", index=False)
print(f"Saved {len(df)} grants from Grants.gov")
