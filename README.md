Gmail API (OAuth)
      ↓
gmail_service.py  → fetch unread → mark read
      ↓
email_parser.py  → extract + clean text
      ↓
main.py          → duplicate check + state
      ↓
sheets_service.py → append rows
      ↓
Google Sheets

# Gmail to Google Sheets Automation

**Author:** Vasanth Kumar  
**Language:** Python 3  
**APIs Used:** Gmail API, Google Sheets API  
**Authentication:** OAuth 2.0  

---

## 📖 Project Overview

This project is a Python automation system that connects to:

• Gmail API  
• Google Sheets API  

The system reads **real incoming unread emails** from a Gmail account and logs them into a Google Sheet.

Each qualifying email is added as a new row with:

| Column | Description |
|--------|-------------|
From | Sender email address
Subject | Email subject
Date | Date & time received
Content | Plain-text email body

---

## 🧠 High-Level Architecture

