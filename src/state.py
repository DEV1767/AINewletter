from typing import Annotated, TypedDict

from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()


class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    papers: list
    ranked_papers: list
    summaries: list
    email_content: str
    documents: list[Document]
    chunks:list[Document]


class RankedPaper(BaseModel):
    title: str
    score: float = Field(
        description="Importance score from 0 to 10"
    )
    reason: str
    pdf_url: str|None=None


class RankedPapers(BaseModel):
    papers: list[RankedPaper]
    
class PaperSummary(BaseModel):
    title: str
    problem: str
    approach: str
    findings: str
    why_it_matters: str


class PaperSummaries(BaseModel):
    summaries: list[PaperSummary]