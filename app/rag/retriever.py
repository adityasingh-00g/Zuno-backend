from app.vectorstore.client import get_vectorstore

def retrieve(state):
    question=state["question"]
    vectorstore=get_vectorstore()
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
    documents=retriever.invoke(question)
    return {"documents":documents,"question":question}