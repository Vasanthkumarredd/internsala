import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SHEETS_SCOPES, CREDENTIALS_PATH, TOKEN_PATH, SHEET_NAME, SERVICE_ACCOUNT_PATH
from google.oauth2.service_account import Credentials as ServiceAccountCredentials



def authenticate_sheets(use_service_account=False):
    """
    Authenticates using OAuth 2.0 (default) or service account if specified.
    Returns Sheets API service.
    """
    if use_service_account:
        if not os.path.exists(SERVICE_ACCOUNT_PATH):
            raise FileNotFoundError(f"Service account file not found: {SERVICE_ACCOUNT_PATH}")
        creds = ServiceAccountCredentials.from_service_account_file(
            SERVICE_ACCOUNT_PATH,
            scopes=SHEETS_SCOPES
        )
        return build("sheets", "v4", credentials=creds)

    # Default: OAuth user authentication
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SHEETS_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SHEETS_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)


def _get_sheet_id(service):
    """
    Returns the spreadsheet ID for the given SHEET_NAME.
    Creates the sheet if it does not exist.
    """
    drive_service = build("drive", "v3", credentials=service._http.credentials)

    response = drive_service.files().list(
        q=f"name='{SHEET_NAME}' and mimeType='application/vnd.google-apps.spreadsheet'",
        spaces="drive"
    ).execute()

    files = response.get("files", [])

    if files:
        return files[0]["id"]

    # Create new spreadsheet
    sheet_metadata = {
        "properties": {
            "title": SHEET_NAME
        }
    }

    spreadsheet = service.spreadsheets().create(body=sheet_metadata).execute()
    return spreadsheet["spreadsheetId"]


def append_rows(service, rows):
    """
    Appends rows to the Google Sheet.
    """
    spreadsheet_id = _get_sheet_id(service)

    body = {
        "values": rows
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()


def ensure_headers(service):
    """
    Ensures header row is always set to: From, Subject, Date, Content.
    Overwrites the first row if it already exists.
    """
    spreadsheet_id = _get_sheet_id(service)
    headers = [["From", "Subject", "Date", "Content"]]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1:D1",
        valueInputOption="RAW",
        body={"values": headers}
    ).execute()
