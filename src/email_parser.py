import base64
from bs4 import BeautifulSoup



def _get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _decode_body(data):
    try:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_body(payload):
    """
    Recursively extracts the email body from the payload.
    """
    if "body" in payload and payload["body"].get("data"):
        return _decode_body(payload["body"]["data"])

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and part["body"].get("data"):
                return _decode_body(part["body"]["data"])
            elif part["mimeType"] == "text/html" and part["body"].get("data"):
                html = _decode_body(part["body"]["data"])
                return html_to_text(html)
            elif "parts" in part:
                return _extract_body(part)

    return ""


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def parse_email(message):
    """
    Parses a Gmail API message object into structured data.
    """
    headers = message["payload"]["headers"]

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date = _get_header(headers, "Date")

    body = _extract_body(message["payload"])

    return {
        "id": message["id"],
        "from": sender,
        "subject": subject,
        "date": date,
        "content": body
    }
