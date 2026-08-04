from langchain_core.messages import HumanMessage
from src.graph import research_graph


initial_state = {
"messages": [
    HumanMessage(
        content=(
            "Find recent high-quality research papers in Artificial Intelligence. "
            "Focus on important and practical AI research such as LLMs, Agentic AI, "
            "Generative AI, RAG, multimodal AI, and AI systems. "
            "Use only ONE broad arXiv search query and return the most relevant papers. "
            "Exclude papers that are not fundamentally related to AI/ML."
        )
    )
],

    "papers": [],
    "ranked_papers": [],
    "summaries": [],
    "email_content": ""
}


result = research_graph.invoke(
    initial_state,
    config={
        "recursion_limit": 10
    }
)


print("\n--- PAPERS FOUND ---")
print(len(result["papers"]))


print("\n--- RANKED PAPERS ---\n")

for paper in result["ranked_papers"]:

    print("Title:", paper.title)
    print("Score:", paper.score)
    print("Reason:", paper.reason)
    print("-" * 60)

print("\n\n========== AI RESEARCH NEWSLETTER ==========\n")

print(result["email_content"])

print("\n============================================")