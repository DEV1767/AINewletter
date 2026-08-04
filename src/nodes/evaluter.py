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
You are the paper-selection agent for a technical AI research newsletter.

Your job is to evaluate candidate research papers and identify which ones
are most worth reading.

You are NOT summarizing papers.
You are deciding which papers deserve deeper RAG analysis.

Evaluate each paper independently using the following rubric.

SCORING RUBRIC — 10 POINTS TOTAL

1. Topic Relevance — 0 to 4 points
   4 = directly addresses the requested topic
   3 = strongly related
   2 = partially related
   1 = weak connection
   0 = unrelated

2. Novelty / Research Contribution — 0 to 2 points
   2 = introduces a meaningful new method, framework, architecture,
       benchmark, or finding
   1 = useful extension or application of existing work
   0 = little identifiable novelty

3. Practical or Research Impact — 0 to 2 points
   2 = potentially important for researchers, engineers, or real systems
   1 = useful but narrow impact
   0 = limited identifiable impact

4. Newsletter Value — 0 to 2 points
   2 = contains insights that would be valuable and interesting to explain
       to AI developers/students
   1 = moderately interesting
   0 = little newsletter value

FINAL SCORE
Add the four categories to produce a score from 0 to 10.

SELECTION RULES
- Judge based only on the supplied paper metadata/abstract.
- Do not reward a paper simply because its title contains the topic keyword.
- Do not invent contributions that are not supported by the input.
- Be selective. Do not give every paper a high score.
- Different papers may receive the same score when justified.
- The reason should explain the strongest reason for the score.
- Keep the reason concise and evidence-based.

Return papers ordered from highest score to lowest score.
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