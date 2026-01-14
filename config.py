
ALL_SCOPES = [
                    "https://www.googleapis.com/auth/gmail.modify",
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]


GMAIL_SCOPES = ALL_SCOPES
SHEETS_SCOPES = ALL_SCOPES

# OAuth files
CREDENTIALS_PATH = "credentials/credentials.json"
TOKEN_PATH = "credentials/token.json"
# Service account file for Sheets
SERVICE_ACCOUNT_PATH = "credentials/service_account.json"


STATE_PATH = "state.json"


SHEET_NAME = "Gmail Logs"


ONLY_UNREAD = True
SUBJECT_FILTER = None  


ENABLE_LOGGING = True
