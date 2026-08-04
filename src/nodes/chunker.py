from src.state import ResearchState
from src.rag.splitter import split_documents

def chunker(state:ResearchState):
    documents=state["documents"]
    
    chunks=split_documents(documents)
    
    print(f"Total pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    
    return {
        "chunks":chunks
    }