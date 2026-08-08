<div align="center">

# 📧 Email Assistant

**AI-powered Gmail assistant built with FastAPI, LangGraph & Gemini**

A smart email assistant that lets you read, search, send, reply, trash, archive and label emails — either through a clean REST API or by chatting with an AI agent that can operate your inbox for you.

</div>

---

## ✨ Features

- 🗂️ **Full Gmail integration** — list, search, read, send, reply, trash, archive, and label emails via the Gmail API
- 🤖 **AI Agent** — a Gemini-powered agent (LangGraph) that understands natural language commands and can call email tools on your behalf
- ⚡ **FastAPI backend** — typed, self-documented REST API with automatic interactive docs (`/docs`)
- 🧠 **Tool-calling agent loop** — the agent automatically decides when to use tools and keeps going until it answers
- 📧 **Smart email parsing** — extracts sender, subject, body, and thread info from raw Gmail messages
- 🔐 **Secure OAuth 2.0** — scoped Google OAuth flow with token refresh

---

## 🛠️ Tech Stack

| Layer        | Technology                                    |
| ------------ | --------------------------------------------- |
| Backend      | [FastAPI](https://fastapi.tiangolo.com/)      |
| AI Agent     | [LangGraph](https://www.langchain.com/langgraph) + LangChain |
| LLM          | Google Gemini (`langchain-google-genai`)      |
| Email        | Google Gmail API                              |
| Validation   | Pydantic v2                                   |
| Auth         | Google OAuth 2.0 (installed app flow)         |

---

## 📁 Project Structure

```
email-assistant/
├── app/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── agent/
│   │   └── graph.py             # LangGraph agent (tools loop)
│   ├── api/
│   │   └── routes/
│   │       ├── agent.py         # /agent/chat endpoint
│   │       └── emails.py        # /emails/* endpoints
│   ├── parsers/
│   │   └── email_parser.py      # Gmail message → EmailDetails
│   ├── schemas/
│   │   ├── agent.py             # Chat request/response models
│   │   └── email.py             # Email & request models
│   ├── services/
│   │   ├── gmail_auth.py        # OAuth auth + Gmail service build
│   │   └── gmail_service.py     # Gmail CRUD operations
│   └── tools/
│       └── email_tools.py       # Tools exposed to the AI agent
├── requirements.txt
└── .env                         # GEMINI_API_KEY (gitignored)
```

---

## 📋 Prerequisites

- Python 3.10+
- A [Google Cloud project](https://console.cloud.google.com/) with the Gmail API enabled
- A [Gemini API key](https://aistudio.google.com/app/apikey)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/email-assistant.git
cd email-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Google Gmail API credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable the **Gmail API**
4. Go to **APIs & Services → Credentials**
5. Create a new **OAuth 2.0 Client ID** (Desktop app)
6. Download the JSON file and save it as `credentials.json` in the project root

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> ⚠️ `credentials.json`, `token.json`, and `.env` are gitignored — never commit them.

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

- Interactive API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/

On first Gmail call, your browser will open an OAuth consent screen. Accept it, and a `token.json` will be created for future sessions.

---

## 🔌 API Endpoints

### 🤖 AI Agent

| Method | Endpoint      | Description                                |
| ------ | ------------- | ------------------------------------------ |
| `POST` | `/agent/chat` | Send a natural-language message to the agent |

**Request:**

```json
{
  "message": "Show me my 3 most recent unread emails from LinkedIn"
}
```

**Response:**

```json
{
  "response": "Here are your 3 most recent emails from LinkedIn..."
}
```

### 📬 Emails

| Method   | Endpoint            | Description                       |
| -------- | ------------------- | --------------------------------- |
| `GET`    | `/emails/`          | List the latest emails            |
| `GET`    | `/emails/search`    | Search emails (`?q=from:...`)     |
| `GET`    | `/emails/labels`    | List all Gmail labels             |
| `GET`    | `/emails/{id}`      | Get a full email by ID            |
| `POST`   | `/emails/send`      | Send a new email                  |
| `POST`   | `/emails/reply`     | Reply to an existing email        |
| `DELETE` | `/emails/trash`     | Move an email to trash            |
| `PATCH`  | `/emails/archive`   | Archive an email                  |
| `PATCH`  | `/emails/label`     | Add a label to an email           |

---

## 🤖 Example Agent Prompts

The agent can understand requests like:

- *"Show me my latest 5 emails"*
- *"Search for emails from GitHub about security alerts"*
- *"Send an email to john@example.com saying the project is ready"*
- *"Reply to the email from Sarah and thank her for the update"*
- *"Move the last email from my bank to trash"*
- *"Archive all emails older than my top 3"*

---

## 🧠 How the Agent Works

The agent is built with **LangGraph** as a simple two-node loop:

```
START → [agent] → tools? → [tools] → [agent] → ... → answer
```

1. The **agent** node sends your message to Gemini with a set of bound tools.
2. If the model wants to act (e.g., send an email), it emits a tool call and execution moves to the **tools** node.
3. Tool results are fed back to the agent, which continues until it produces a final answer.

The agent's tools mirror the email API: `search_emails`, `get_email`, `send_email`, `reply_to_email`, `trash_email`, `archive_email`, `add_label`, `list_labels`.

---

## 🧪 Running the Agent Locally

To test the agent from the command line, uncomment the `if __name__ == "__main__":` block in `app/agent/graph.py` and run:

```bash
python -m app.agent.graph
```

---

## 🔒 Security Notes

- The Gmail integration uses the **`gmail.modify`** scope — read, send, and modify (no permanent delete).
- OAuth tokens are stored locally in `token.json` and refreshed automatically.
- Keep your `GEMINI_API_KEY`, `credentials.json`, and `token.json` out of version control (already covered by `.gitignore`).

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use it in your own projects.
