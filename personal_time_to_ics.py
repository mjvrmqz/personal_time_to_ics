#!/usr/bin/env python3
import os
import requests
from datetime import datetime, timezone
from ics import Calendar, Event

# === CONFIG ===
NOTION_TOKEN = "ntn_E87966143344ZHA3FlZrEvMiblhvgFoQWNtGqLaa9JnbSm"
DATABASE_ID = "2aa20c51aebe80439c52e60fdf45dd31"  # replace with your personal time database ID

# === FUNCTIONS ===
def notion_query_database(token, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Notion API error {resp.status_code}: {resp.text}")
    return resp.json()["results"]

def create_ics(events):
    cal = Calendar()
    for event in events:
        try:
            title = event["properties"][" Calendar"]["title"][0]["plain_text"]
            start = event["properties"]["Time"]["date"]["start"]
            end = event["properties"]["Time"]["date"].get("end", start)
            
            # Safe check for Actionable Steps
            steps_list = event["properties"]["Actionable Steps"]["rich_text"]
            description = steps_list[0]["plain_text"] if steps_list else ""
            
        except KeyError:
            continue  # Skip events missing the required columns
        e = Event()
        e.name = title
        e.begin = start
        e.end = end
        e.description = description
        cal.events.add(e)
    with open("personal_time_feed.ics", "w") as f:
        f.writelines(cal)

def main():
    events = notion_query_database(NOTION_TOKEN, DATABASE_ID)
    create_ics(events)
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"ICS feed updated at {now}")

if __name__ == "__main__":
    main()