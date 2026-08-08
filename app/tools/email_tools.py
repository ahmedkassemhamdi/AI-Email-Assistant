from langchain_core.tools import tool

from app.services.gmail_service import GmailService


gmail = GmailService()


@tool
def search_emails(query: str, max_results: int = 10):
    """
    Search emails in Gmail using a Gmail search query.
    Example: from:linkedin.com
    """
    return gmail.search_emails(
        query=query,
        max_results=max_results
    )


@tool
def get_email(message_id: str):
    """
    Get the full details of a specific email using its message ID.
    """
    return gmail.get_message(message_id)


@tool
def send_email(to: str, subject: str, body: str):
    """
    Send an email to a recipient.
    """
    return gmail.send_email(
        to=to,
        subject=subject,
        body=body
    )


@tool
def reply_to_email(
    message_id: str,
    to: str,
    subject: str,
    body: str
):
    """
    Reply to an existing email.
    """
    return gmail.reply_email(
        message_id=message_id,
        to=to,
        subject=subject,
        body=body
    )


@tool
def trash_email(message_id: str):
    """
    Move an email to the Gmail trash.
    """
    return gmail.trash_email(
        message_id=message_id
    )


@tool
def archive_email(message_id: str):
    """
    Archive an email by removing it from the inbox.
    """
    return gmail.archive_email(
        message_id=message_id
    )


@tool
def add_label(message_id: str, label_id: str):
    """
    Add a Gmail label to an email.
    """
    return gmail.add_label(
        message_id=message_id,
        label_id=label_id
    )


@tool
def list_labels():
    """
    Get all available Gmail labels.
    """
    return gmail.list_labels()

email_tools = [
    search_emails,
    get_email,
    send_email,
    reply_to_email,
    trash_email,
    archive_email,
    add_label,
    list_labels,
]

