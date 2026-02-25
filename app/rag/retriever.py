from app.vectorstore.client import get_vectorstore
from app.rag.reranker import rerank

def retrieve(state):
    question=state["question"]
    user_id=state["user_id"]
    vectorstore=get_vectorstore()
    #retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
    #documents=retriever.invoke(question)
    documents=vectorstore.similarity_search(
        query=question,
        k=10,
        filter={"user_id":user_id}
    )
    print("Question : ",question)
    print("Retrieved docs : ",documents)
    reranked_documents=rerank(question,documents,top_k=3)
    return {"documents":reranked_documents,"question":question}