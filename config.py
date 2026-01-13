                # Unified scopes for Gmail, Sheets, and Drive
ALL_SCOPES = [
                    "https://www.googleapis.com/auth/gmail.modify",
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]

                # Use unified scopes for both Gmail and Sheets
GMAIL_SCOPES = ALL_SCOPES
SHEETS_SCOPES = ALL_SCOPES

# OAuth files
CREDENTIALS_PATH = "credentials/credentials.json"
TOKEN_PATH = "credentials/token.json"
# Service account file for Sheets
SERVICE_ACCOUNT_PATH = "credentials/service_account.json"

# State persistence
STATE_PATH = "state.json"

# Sheet name
SHEET_NAME = "Gmail Logs"

# Filters
ONLY_UNREAD = True
SUBJECT_FILTER = None  # e.g., "Invoice"

# Logging
ENABLE_LOGGING = True
