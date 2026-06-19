import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os
from datetime import datetime

# Load credentials from GitHub secret
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_json, scopes=[
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
])

client = gspread.authorize(creds)
workbook = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])

def write_tab(workbook, tab_name, df, headers):
    # Get existing tab or create it
    try:
        tab = workbook.worksheet(tab_name)
        tab.clear()
    except gspread.exceptions.WorksheetNotFound:
        tab = workbook.add_worksheet(title=tab_name, rows=500, cols=20)

    # Write header row
    tab.append_row(headers)

    # Only keep columns that exist in the dataframe
    existing_headers = [h for h in headers if h in df.columns]
    rows = df[existing_headers].fillna("").values.tolist()

    # Write in batches of 50 to stay within Sheets API limits
    batch_size = 50
    for i in range(0, len(rows), batch_size):
        tab.append_rows(rows[i:i + batch_size])

    print(f"Written {len(rows)} rows to tab: {tab_name}")

# Tab 1 — Grant Opportunities (refreshed every run)
try:
    grants = pd.read_csv("filtered_grants.csv")
    write_tab(workbook, "Grant Opportunities", grants, [
        "funder", "program", "award_floor", "award_ceiling",
        "deadline", "post_date", "matched_tags", "relevance_score",
        "description", "url", "date_pulled"
    ])
except FileNotFoundError:
    print("filtered_grants.csv not found — skipping")

# Tab 2 — Foundations to Research (refreshed every run)
try:
    foundations = pd.read_csv("filtered_foundations.csv")
    write_tab(workbook, "Foundations to Research", foundations, [
        "funder", "city", "state", "revenue", "assets",
        "matched_tags", "relevance_score", "propublica_url", "date_pulled"
    ])
except FileNotFoundError:
    print("filtered_foundations.csv not found — skipping")

# Tab 3 — Application Tracker (created once, never overwritten)
try:
    workbook.worksheet("Application Tracker")
    print("Application Tracker already exists — skipping")
except gspread.exceptions.WorksheetNotFound:
    tracker = workbook.add_worksheet(
        title="Application Tracker", rows=100, cols=15
    )
    tracker.append_row([
        "Funder", "Program", "Amount", "Deadline", "Status",
        "Point of Contact", "Date Applied", "Decision", "Notes", "URL"
    ])
    print("Created Application Tracker tab")

# Tab 4 — Run Log (appends a new row every run)
try:
    log = workbook.worksheet("Run Log")
except gspread.exceptions.WorksheetNotFound:
    log = workbook.add_worksheet(title="Run Log", rows=100, cols=5)
    log.append_row(["Run Date", "Grants Found", "Foundations Found", "Status"])

grants_count = len(pd.read_csv("filtered_grants.csv")) \
    if os.path.exists("filtered_grants.csv") else 0
found_count  = len(pd.read_csv("filtered_foundations.csv")) \
    if os.path.exists("filtered_foundations.csv") else 0

log.append_row([
    datetime.today().strftime("%Y-%m-%d %H:%M UTC"),
    grants_count,
    found_count,
    "Success"
])
print("Run logged successfully")
