from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START
from dotenv import load_dotenv
from app.tools.email_tools import email_tools
from langchain_core.messages import HumanMessage


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    api_key=api_key
)

model_with_tools = model.bind_tools(email_tools)


def call_model(state: AgentState):

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(email_tools)
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()



# if __name__ == "__main__":

#     result = graph.invoke({
#         "messages": [
#             HumanMessage(content="Show me my latest 5 emails")
#         ]
#     })

#     final_message = result["messages"][-1]

#     if isinstance(final_message.content, list):
#         for item in final_message.content:
#             if item.get("type") == "text":
#                 print(item["text"])
#     else:
#         print(final_message.content)
