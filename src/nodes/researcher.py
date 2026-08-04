import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from src.tools.arxiv import search_arxiv


model1 = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY_2")
)

tools = [search_arxiv]

model1_with_tool = model1.bind_tools(tools)


def researcher(state):

    system_message = SystemMessage(
        content="""
        You are an AI research assistant.

        Find recent AI research papers related to Agentic AI.

        Use the arXiv search tool when needed.
        Once the tool has returned papers, DO NOT search again.
        Analyze the returned results and give your final response.
        """
    )

    messages = [
        system_message,
        *state["messages"]
    ]

    response = model1_with_tool.invoke(messages)

    return {
        "messages": [response]
    }