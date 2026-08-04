from src.state import ResearchState
from src.tools.pdf_loader import load_pdf

def pdf_loader(state:ResearchState):
    top_paper=state['ranked_papers'][:3]
    
    documents=[]
    
    for paper in top_paper:
        docs=load_pdf(paper.pdf_url)
        
        for doc in docs:
            doc.metadata["paper_title"]=paper.title
            doc.metadata["pdf_url"]=paper.pdf_url
            
        documents.extend(docs)
        print(f"\nTotal pages loaded: {len(documents)}")

    return {
      'documents':documents
  }