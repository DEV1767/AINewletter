from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from src.state import ResearchState
from src.nodes.researcher import researcher
from src.tools.arxiv import search_arxiv
from src.nodes.evaluter import evaluator
from src.nodes.pdf_loader import pdf_loader
from src.nodes.chunker import chunker
from src.nodes.summarizer import paper_summarizer
from src.nodes.newsletter import newsletter_writer
from src.nodes.email_sender import email_sender


tools = [search_arxiv]

builder = StateGraph(ResearchState)




builder.add_node("researcher", researcher)
builder.add_node("tools", ToolNode(tools))
builder.add_node("evaluator", evaluator)
builder.add_node("pdf_loader", pdf_loader)
builder.add_node("chunker", chunker)
builder.add_node("summarizer", paper_summarizer)
builder.add_node("newsletter", newsletter_writer)
builder.add_node("email_sender", email_sender)



builder.add_edge(START, "researcher")


def researcher_router(state: ResearchState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "evaluator"


builder.add_conditional_edges(
    "researcher",
    researcher_router,
    {
        "tools": "tools",
        "evaluator": "evaluator"
    }
)


builder.add_edge("tools", "researcher")
builder.add_edge("evaluator", "pdf_loader")
builder.add_edge("pdf_loader", "chunker")
builder.add_edge("chunker", "summarizer")
builder.add_edge("summarizer", "newsletter")
builder.add_edge("newsletter", "email_sender")
builder.add_edge("email_sender", END)

research_graph = builder.compile()