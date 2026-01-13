import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import GMAIL_SCOPES, CREDENTIALS_PATH, TOKEN_PATH, ONLY_UNREAD, SUBJECT_FILTER


def authenticate_gmail():
    """
    Authenticates the user via OAuth 2.0 and returns a Gmail API service.
    """
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, GMAIL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def fetch_unread_messages(service, max_results=20):
    """
    Fetches unread emails (optionally filtered by subject).
    Returns a list of Gmail message objects.
    """
    query_parts = []

    if ONLY_UNREAD:
        query_parts.append("is:unread")

    if SUBJECT_FILTER:
        query_parts.append(f"subject:{SUBJECT_FILTER}")

    query = " ".join(query_parts)

    response = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])
    full_messages = []

    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        full_messages.append(full_msg)

    return full_messages


def mark_as_read(service, message_id):
    """
    Removes the UNREAD label from a message.
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
