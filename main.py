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
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def generate_order_number():
    # First block: 400-499
    first = random.randint(400, 499)

    # Second and third blocks: 7 digits each
    second = random.randint(1000000, 9999999)
    third = random.randint(1000000, 9999999)

    return f"{first}-{second}-{third}"


def create_draft(service, to_email, subject, body):
    message = MIMEText(body)

    # Leave this blank if you don't want a recipient
    if to_email:
        message["to"] = to_email

    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

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

    # Leave blank if you don't want any recipient
    recipient = "ofm@amazon.in"

    used_order_numbers = set()

    for i in range(100):

        # Generate a unique order number
        while True:
            order_number = generate_order_number()
            if order_number not in used_order_numbers:
                used_order_numbers.add(order_number)
                break

        subject = order_number
        body = ""

        create_draft(service, recipient, subject, body)

        print(f"Created draft {i + 1}: {order_number}")

    print("Done! 100 drafts created.")


if __name__ == "__main__":
    main()
