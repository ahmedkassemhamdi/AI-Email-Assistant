from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    id: str
    sender: str
    subject: str
    date: str
    snippet: str


class EmailDetails(Email):
    thread_id: str
    recipient: str
    body: str


class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str


class ReplyEmailRequest(BaseModel):
    message_id: str
    to: EmailStr
    subject: str
    body: str


class TrashEmailRequest(BaseModel):
    message_id: str

class ArchiveEmailRequest(BaseModel):
    message_id: str
    