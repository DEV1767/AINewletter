import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import ResearchState, PaperSummary
from src.rag.retriver import retrieve_for_paper
from src.rag.vectorstore import create_vectorstores


model1 = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY_2")
)

summary_model = model1.with_structured_output(PaperSummary)


def paper_summarizer(state: ResearchState):

    chunks = state["chunks"]
    top_papers = state["ranked_papers"][:3]

    # Create separate FAISS store for each paper
    vectorstores = create_vectorstores(chunks)

    summaries = []

    for paper in top_papers:

        print(f"\nSummarizing: {paper.title}")

        docs = retrieve_for_paper(
            vectorstores=vectorstores,
            paper_title=paper.title,
            query="""
            What is the main problem, proposed approach,
            important findings, results and practical significance
            of this research?
            """,
            k=6
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        response = summary_model.invoke([
            system_prompt = """
You are a research-paper analysis agent in a RAG pipeline.

Your task is to produce an accurate technical summary using ONLY the
retrieved context from the research paper.

GROUNDING RULES

1. Treat the retrieved context as the only source of truth.
2. Do not use outside knowledge to fill missing information.
3. Do not invent experiments, metrics, datasets, architectures, results,
   limitations, or conclusions.
4. If the retrieved context does not contain enough evidence for a field,
   explicitly state that the available context does not provide enough
   information.
5. Distinguish clearly between what the authors propose and what their
   experiments demonstrate.
6. Preserve important technical terminology from the paper.
7. Include quantitative results only when explicitly present in the context.

ANALYSIS GOAL

Extract the information a technical reader needs to understand:

- What problem the paper addresses
- Why that problem matters
- What the authors propose
- How the proposed approach works
- What the experiments/findings demonstrate
- Why the work matters for AI researchers or engineers

STYLE

- Concise but technically meaningful
- No marketing language
- No exaggerated claims
- Explain specialized concepts clearly
- Prefer concrete findings over generic statements
- Avoid repeating the paper title as an explanation

Return the required structured output only.
""",

            HumanMessage(
                content=f"""
                Paper title:
                {paper.title}

                Retrieved paper context:
                {context}
                """
            )
        ])

        summaries.append(response)

    return {
        "summaries": summaries
    }