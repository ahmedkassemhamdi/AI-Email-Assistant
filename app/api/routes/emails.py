from fastapi import APIRouter, Query
from app.services.gmail_service import GmailService
from app.schemas.email import SendEmailRequest, ReplyEmailRequest, TrashEmailRequest, ArchiveEmailRequest

router = APIRouter(prefix="/emails", tags=["Emails"])

gmail = GmailService()


@router.get("/")
def list_emails():

    return gmail.list_emails()

@router.get("/search")
def search_emails(
    q: str = Query(...),
    max_results: int = 10
):


    return gmail.search_emails(
        query=q,
        max_results=max_results
    )

@router.get("/labels")
def get_labels():

    return gmail.list_labels()

@router.get("/{message_id}")
def get_email(message_id: str):

    return gmail.get_message(message_id)

@router.post("/send")
def send_email(request: SendEmailRequest):


    result = gmail.send_email(
        to=request.to,
        subject=request.subject,
        body=request.body,
    )

    return result

@router.post("/reply")
def reply_email(request: ReplyEmailRequest):
    return gmail.reply_email(
        message_id=request.message_id,
        to=request.to,
        subject=request.subject,
        body=request.body,
    )

@router.delete("/trash")
def trash_email(request: TrashEmailRequest):

    return gmail.trash_email(
        message_id=request.message_id
    )

@router.patch("/archive")
def archive_email(request: ArchiveEmailRequest):

    return gmail.archive_email(
        message_id=request.message_id
    )

@router.patch("/label")
def add_label(
    message_id: str,
    label_id: str
):
    return gmail.add_label(
        message_id=message_id,
        label_id=label_id
    )
