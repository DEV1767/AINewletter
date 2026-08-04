def retrieve_for_paper(
    vectorstores,
    paper_title: str,
    query: str,
    k: int = 4
):

  
    vectorstore = vectorstores.get(paper_title)

    if vectorstore is None:
        return []

 
    documents = vectorstore.similarity_search(
        query,
        k=k
    )

    return documents


def retriver_for_paper(
    vectorstores,
    paper_title: str,
    query: str,
    k: int = 4
):
    return retrieve_for_paper(
        vectorstores=vectorstores,
        paper_title=paper_title,
        query=query,
        k=k
    )