import os
import base64
import random
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail permission
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            # Manual authentication (no localhost required)
            creds = flow.run_console()

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def generate_order_number():
    first = random.randint(400, 499)
    second = random.randint(1000000, 9999999)
    third = random.randint(1000000, 9999999)

    return f"{first}-{second}-{third}"


def create_draft(service, to_email, subject, body):

    message = MIMEText(body)

    if to_email:
        message["to"] = to_email

    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft = {
        "message": {
            "raw": raw
        }
    }

    service.users().drafts().create(
        userId="me",
        body=draft
    ).execute()


def main():

    service = gmail_service()

    recipient = "ofm@amazon.in"

    used = set()

    NUMBER_OF_DRAFTS = 100

    for i in range(NUMBER_OF_DRAFTS):

        while True:
            order = generate_order_number()

            if order not in used:
                used.add(order)
                break

        create_draft(
            service,
            recipient,
            order,
            ""
        )

        print(f"Created draft {i+1}: {order}")

    print("Done! All drafts created.")


if __name__ == "__main__":
    main()
