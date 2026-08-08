from app.services.gmail_auth import authenticate
from app.schemas.email import Email
from app.parsers.email_parser import EmailParser
import base64
from email.mime.text import MIMEText


class GmailService:

    def __init__(self):
        self.service = authenticate()
    # ===================================================

    def list_messages(self, max_results=10):

        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results
            )
            .execute()
        )

        messages = results.get("messages", [])

        return messages
    # ===================================================

    def get_raw_message(self, message_id: str):

        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )
    # ===================================================

    def get_message(self, message_id: str):

        message = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )

        return EmailParser.parse(message)

    # ===================================================

    def list_emails(self, max_results: int = 10) -> list[Email]:
        messages = self.list_messages(max_results)

        emails = []

        for message in messages:
            email = self.get_message(message["id"])
            emails.append(email)

        return emails


    # ===================================================

    def send_email(
        self,
        to: str,
        subject: str,
        body: str
        ):

        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        sent_message = (
            self.service.users()
            .messages()
            .send(
                userId="me",
                body={
                    "raw": raw
                }
            )
            .execute()
        )

        return sent_message
    # ===================================================

    def search_messages(self, query: str, max_results: int = 10):

        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results
            )
            .execute()
        )

        return results.get("messages", [])
    # ===================================================

    def search_emails(self, query: str, max_results: int = 10):

        messages = self.search_messages(
            query=query,
            max_results=max_results
        )

        emails = []

        for message in messages:
            email = self.get_message(message["id"])
            emails.append(email)

        return emails
    # ===================================================

    def reply_email(
        self,
        message_id: str,
        to: str,
        subject: str,
        body: str
    ):

        original = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata"
            )
            .execute()
        )

        headers = original["payload"]["headers"]

        message_id_header = ""

        for header in headers:
            if header["name"] == "Message-ID":
                message_id_header = header["value"]

        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject
        message["In-Reply-To"] = message_id_header
        message["References"] = message_id_header

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        return (
            self.service.users()
            .messages()
            .send(
                userId="me",
                body={
                    "raw": raw,
                    "threadId": original["threadId"]
                }
            )
            .execute()
        )    

# ===================================================

    def trash_email(self, message_id: str):

        return (
            self.service.users()
            .messages()
            .trash(
                userId="me",
                id=message_id
            )
            .execute()
        )

# ===================================================

    def archive_email(self, message_id: str):

        return (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={
                    "removeLabelIds": ["INBOX"]
                }
            )
            .execute()
        )

# ===================================================

    def list_labels(self):

        results = (
            self.service.users()
            .labels()
            .list(
                userId="me"
            )
            .execute()
        )

        return results.get("labels", [])

# ===================================================

    def add_label(self, message_id: str, label_id: str):

        result = (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={
                    "addLabelIds": [label_id]
                }
            )
            .execute()
        )

        return result

