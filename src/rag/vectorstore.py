from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def create_vectorstores(chunks):

    # Group chunks according to paper
    papers = {}

    for chunk in chunks:

        paper_title = chunk.metadata.get("paper_title")

        if paper_title not in papers:
            papers[paper_title] = []

        papers[paper_title].append(chunk)


    # Create separate FAISS for every paper
    vectorstores = {}

    for paper_title, paper_chunks in papers.items():

        print(
            f"Creating vector store for: {paper_title}"
        )

        print(
            f"Chunks: {len(paper_chunks)}"
        )

        vectorstore = FAISS.from_documents(
            documents=paper_chunks,
            embedding=embeddings
        )

        vectorstores[paper_title] = vectorstore

    return vectorstores