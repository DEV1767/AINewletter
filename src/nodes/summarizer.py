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
            SystemMessage(
                content="""
                You are an AI research paper analyst.

                Analyze the provided retrieved sections of a
                research paper.

                Only use information present in the provided context.
                Do not invent results or claims.

                Explain the research clearly and concisely.
                """
            ),

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