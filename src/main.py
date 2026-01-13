import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmail_service import authenticate_gmail, fetch_unread_messages, mark_as_read
from sheets_service import authenticate_sheets, append_rows, ensure_headers
from email_parser import parse_email
from config import STATE_PATH, ENABLE_LOGGING


def load_state():
    if not os.path.exists(STATE_PATH):
        return {"processed_email_ids": []}

    with open(STATE_PATH, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def log(message):
    if ENABLE_LOGGING:
        print(message)


def main():

    # Set to True to use service account for Sheets
    USE_SERVICE_ACCOUNT = True

    log(" Authenticating Sheets...")
    sheets_service = authenticate_sheets(use_service_account=USE_SERVICE_ACCOUNT)

    log(" Authenticating Gmail...")
    gmail_service = authenticate_gmail()

    log(" Ensuring headers...")
    ensure_headers(sheets_service)

    log(" Fetching unread emails...")
    messages = fetch_unread_messages(gmail_service)
    from config import STATE_PATH, ENABLE_LOGGING
    state = load_state()
    processed_ids = set(state.get("processed_email_ids", []))

    new_rows = []

    for msg in messages:
        # Extract headers and plain text body
        headers = msg["payload"]["headers"]
        data = {"From": "", "Subject": "", "Date": ""}
        for h in headers:
            if h["name"] == "From":
                data["From"] = h["value"]
            elif h["name"] == "Subject":
                data["Subject"] = h["value"]
            elif h["name"] == "Date":
                data["Date"] = h["value"]

        # Use message id for deduplication
        msg_id = msg["id"]
        if msg_id in processed_ids:
            log(f" Skipping duplicate: {data['Subject']}")
            continue

        # Extract plain text body (reuse parse_email for body extraction)
        body = parse_email(msg)["content"]
        max_cell_length = 200
        content = body[:max_cell_length] if body else ""

        new_rows.append([
            data["From"],
            data["Subject"],
            data["Date"],
            data["Content"] if "Content" in data else content
        ])

        processed_ids.add(msg_id)
        mark_as_read(gmail_service, msg_id)
        log(f" Processed: {data['Subject']}")

    if new_rows:
        log(f" Appending {len(new_rows)} new rows...")
        append_rows(sheets_service, new_rows)
    else:
        log("📭 No new emails to process.")

    state["processed_email_ids"] = list(processed_ids)
    save_state(state)

    log(" State saved.")
    log(" Done!")


if __name__ == "__main__":
    main()
