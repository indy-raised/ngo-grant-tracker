# NGO Grant Tracker Pipeline

An automated data pipeline that discovers and filters grant 
opportunities for Shadows Project, a Ukrainian cultural heritage 
NGO. The pipeline pulls from public grant databases, scores 
results by relevance, and writes to a shared Google Sheet 
updated automatically every month.

Built and maintained by Anne who volunteers for
finance and grants work for Shadows Project.

---

## What It Does

- Pulls open grant opportunities from the Grants.gov public API
- Pulls arts and culture foundation data from the ProPublica 
  Nonprofit Explorer API
- Scores and filters every result by relevance to Shadows Project 
  using a weighted keyword system across 17 tags including Ukraine, 
  cultural preservation, heritage, human rights, arts, displacement, 
  and more
- Writes filtered results to a shared Google Sheet with four tabs
- Runs automatically on the 1st of every month via GitHub Actions
  with no manual intervention needed

---

## Tech Stack

- Python 3.11
- GitHub Actions (automated monthly scheduling)
- Google Sheets API + Google Drive API
- Grants.gov REST API (public, no key required)
- ProPublica Nonprofit Explorer API (public, no key required)
- pandas, gspread, google-auth, requests

---

## Repo Structure

ngo-grant-tracker/

├── .github/

│   └── workflows/

│       └── run_grants.yml        # scheduler and pipeline runner

├── scripts/

│   ├── fetch_grants_gov.py       # pulls from Grants.gov API

│   ├── fetch_990s.py             # pulls from ProPublica API

│   └── filter.py                 # scores and filters results

├── output/

│   └── push_to_sheets.py         # writes to Google Sheet

├── .gitignore

├── requirements.txt

└── README.md

---

## How the Relevance Scoring Works

Each grant or foundation is scored based on how many 
Shadows-relevant keywords appear in the title, description, 
and funder name. Keywords are weighted by priority:

| Keyword | Points |
|---|---|
| Ukraine | 5 |
| Cultural, Heritage, Preservation | 4 each |
| Arts, Museum, Displacement, Refugee, Human Rights, Eastern Europe, War, Conflict | 3 each |
| Youth, Activism, Digital, Identity | 2 each |
| Community | 1 |

Grants scoring 3 or above appear in the output. 
Results are sorted highest score first.

---

## Google Sheet Output

The pipeline writes to a shared Google Sheet with four tabs:

| Tab | Contents | Refreshes? |
|---|---|---|
| Grant Opportunities | Filtered Grants.gov results | Yes — monthly |
| Foundations to Research | Arts/culture foundations from ProPublica | Yes — monthly |
| Application Tracker | Manual tracker for the grants team | Never — safe to edit |
| Run Log | Timestamp and count for each pipeline run | Appends only |

---

## Setup (for contributors or anyone forking this repo)

1. Clone the repo to your GitHub account
2. Go to Google Cloud Console and create a new project
3. Enable the Google Sheets API and Google Drive API
4. Create a service account and download the credentials JSON
5. Add two GitHub repository secrets:
   - `GOOGLE_CREDENTIALS` — full contents of the credentials JSON file
   - `GOOGLE_SHEET_ID` — the ID string from your Google Sheet URL
6. Share your Google Sheet with the service account email as Editor
7. Go to Actions → Monthly Grant Refresh → Run workflow to test

---

## Important Notes for Editors

- Do not manually edit the Grant Opportunities or Foundations 
  to Research tabs — changes will be overwritten on the next run
- Use the Application Tracker tab to save and track grants 
  the team is actively pursuing
- The Run Log tab shows the date and time of every pipeline 
  run and how many results were found

---

## About Shadows Project

Shadows Project is a Ukrainian cultural heritage NGO working 
to preserve and promote Ukrainian national identity through 
research, storytelling, and design. Learn more at 
[shadowsproject.org](https://shadowsproject.org)
