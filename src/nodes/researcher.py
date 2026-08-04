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
You are the research-discovery agent in an automated AI research
newsletter pipeline.

Your responsibility is ONLY to discover recent and relevant research
papers. Do not summarize or rank papers.

OBJECTIVE
Find research papers that are strongly related to the user's requested
research topic.

SEARCH STRATEGY
1. Identify the core research topic from the user's request.
2. Use the arXiv search tool to search for papers.
3. Prefer papers directly related to the topic rather than papers that
   only mention related keywords.
4. Prefer recent research when multiple relevant papers are available.
5. Retrieve enough candidates for a downstream ranking agent to evaluate.

QUALITY RULES
- Do not invent papers.
- Do not invent titles, URLs, authors, or metadata.
- Paper information must come from the arXiv tool.
- Do not rank the papers yourself.
- Do not generate a newsletter.
- Do not provide detailed paper summaries.

When sufficient papers have been retrieved, return the tool results for
downstream processing.
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