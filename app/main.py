from fastapi import FastAPI

from app.api.routes import emails
from app.api.routes import agent


app = FastAPI(
    title="Email Assistant API",
    description="AI-powered Email Assistant using Gmail API and LangGraph",
    version="1.0.0"
)


# Gmail endpoints
app.include_router(emails.router)

# AI Agent endpoint
app.include_router(agent.router)


@app.get("/")
def root():
    return {
        "message": "Email Assistant API is running"
    }
