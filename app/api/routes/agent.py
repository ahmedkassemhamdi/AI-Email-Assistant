from fastapi import APIRouter

from app.schemas.agent import AgentRequest, AgentResponse
from app.agent.graph import graph

from langchain_core.messages import HumanMessage


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.post("/chat", response_model=AgentResponse)
def chat(request: AgentRequest):

    result = graph.invoke({
        "messages": [
            HumanMessage(content=request.message)
        ]
    })

    final_message = result["messages"][-1]

    if isinstance(final_message.content, list):
        text = ""

        for item in final_message.content:
            if item.get("type") == "text":
                text += item["text"]

    else:
        text = final_message.content

    return {
        "response": text
    }
