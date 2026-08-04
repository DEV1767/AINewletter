from langchain_core.messages import HumanMessage
from src.graph import research_graph


initial_state = {

    "messages": [
        HumanMessage(
            content=(
                "Find recent, high-quality research papers strictly within the field of "
                "Artificial Intelligence (AI). This includes all major AI subfields such as: "
                "Large Language Models (LLMs), Agentic AI and AI agents, Machine Learning, "
                "Deep Learning, Reinforcement Learning, Natural Language Processing (NLP), "
                "Computer Vision, Multimodal AI, Generative AI, AI Safety and Alignment, "
                "Retrieval-Augmented Generation (RAG), Model efficiency/optimization, and "
                "AI systems/infrastructure research. Do not restrict results to only one "
                "subfield (e.g. do not fetch only agentic AI papers) — cover the breadth of "
                "current AI research so no important paper from a major subfield is missed. "
                "Exclude papers that are not fundamentally about AI/ML (e.g. purely "
                "unrelated physics, biology, or general software engineering papers that "
                "don't involve AI/ML methods)."
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