import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import ResearchState, RankedPapers

llm= ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY_1")
)

evaluator_llm = llm.with_structured_output(RankedPapers)


def evaluator(state: ResearchState):

    papers = state["papers"]

    system_message = SystemMessage(
        content="""
        You are an AI research paper evaluator.

        Evaluate and rank the provided research papers.

        Consider:
        1. Relevance to Agentic AI, Generative AI, and AI
        2. Novelty of the research
        3. Practical usefulness
        4. Potential impact

        Give each paper a score from 0 to 10.

        Return the papers ordered from highest score
        to lowest score.
        """
    )

    human_message = HumanMessage(
        content=str(papers)
    )

    response = evaluator_llm.invoke([
        system_message,
        human_message
    ])

    return {
        "ranked_papers": response.papers
    }