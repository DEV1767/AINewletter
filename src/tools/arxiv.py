import time
import arxiv

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId

from langgraph.types import Command
from typing_extensions import Annotated


@tool
def search_arxiv(
    query: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
    max_results: int = 10
) -> Command:
    """Search arXiv for recent research papers."""

    print(f"Searching: {query}")

    start = time.time()

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max(1, min(int(max_results), 10)),
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []

    for result in client.results(search):

        papers.append({
            "title": result.title,
            "abstract": result.summary,
            "published": str(result.published),
            "pdf_url": result.pdf_url
        })

    print(f"arXiv took: {time.time() - start:.2f} seconds")

    return Command(
        update={
            "papers": papers,

            "messages": [
                ToolMessage(
                    content=f"Found {len(papers)} recent research papers.",
                    tool_call_id=tool_call_id
                )
            ]
        }
    )