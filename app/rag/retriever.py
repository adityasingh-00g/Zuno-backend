from app.vectorstore.client import get_vectorstore
from app.rag.reranker import rerank
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

def retrieve(state):
    question=state["question"]
    user_id=state["user_id"]
    vectorstore=get_vectorstore()
    #retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
    #documents=retriever.invoke(question)
    #vectorstore retrieval
    documents_vector=vectorstore.similarity_search(
        query=question,
        k=10,
        filter={"user_id":user_id}
    )
    docs_data = vectorstore.get(where={"user_id": user_id})

    documents = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(docs_data["documents"], docs_data["metadatas"])
    ]

    # BM25 retrieval
    k=10
    tokenized_docs = [doc.page_content.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query=question.split()
    bm25_scores=bm25.get_scores(tokenized_query)
    bm25_top_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True
    )[:min(k,len(bm25_scores))]
    bm25_docs = [documents[i] for i in bm25_top_indices]
    combined_docs=[doc for doc in documents_vector+bm25_docs]
    print("Question : ",question)
    print("Retrieved docs : ",combined_docs)
    reranked_documents=rerank(question,combined_docs,top_k=3)
    print("Reranked doc : ",reranked_documents)
    return {"documents":reranked_documents,"question":question}
