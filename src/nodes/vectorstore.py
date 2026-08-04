from src.state import ResearchState
from src.rag.vectorstore import create_vectorstores
from src.rag.retriver import retrieve_for_paper


def vectorstore_node(state: ResearchState):

    chunks = state["chunks"]

    print(f"\nCreating embeddings for {len(chunks)} chunks...")

   
    vectorstores = create_vectorstores(chunks)

    print("\nVector stores created successfully")

    
    paper = state["ranked_papers"][0]

    print("\nTesting retrieval for:")
    print(paper.title)

    docs = retrieve_for_paper(
        vectorstores=vectorstores,
        paper_title=paper.title,
        query="What is the main contribution and proposed method of this research?",
        k=3
    )

    print(f"\nRetrieved chunks: {len(docs)}")

    for doc in docs:
        print("\n--- CHUNK ---")
        print("Paper:", doc.metadata.get("paper_title"))
        print("Page:", doc.metadata.get("page"))
        print(doc.page_content[:500])

    return {}