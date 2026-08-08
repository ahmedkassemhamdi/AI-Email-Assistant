import base64

from app.schemas.email import EmailDetails

class EmailParser:

    @staticmethod
    def get_header(headers, name):
        for header in headers:
            if header["name"] == name:
                return header["value"]

        return ""

    @staticmethod
    def extract_body(parts):
        if not parts:
            return ""

        for part in parts:

            if part.get("mimeType") == "text/plain":

                data = part.get("body", {}).get("data")

                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")

            if "parts" in part:
                body = EmailParser.extract_body(part["parts"])

                if body:
                    return body

        return ""

    @staticmethod
    def parse(message):

        payload = message.get("payload", {})
        headers = payload.get("headers", [])

        parts = payload.get("parts", [])

        body = ""

        if parts:
            body = EmailParser.extract_body(parts)
        else:
            data = payload.get("body", {}).get("data")

            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")

        return EmailDetails(
            id=message.get("id"),
            thread_id=message.get("threadId"),
            subject=EmailParser.get_header(headers, "Subject"),
            sender=EmailParser.get_header(headers, "From"),
            recipient=EmailParser.get_header(headers, "To"),
            date=EmailParser.get_header(headers, "Date"),
            snippet=message.get("snippet", ""),
            body=body,
        )
    