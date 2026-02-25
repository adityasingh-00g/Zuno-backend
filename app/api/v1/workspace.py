from app.vectorstore.client import get_vectorstore
from langchain_core.documents import Document
from fastapi import APIRouter,Depends
from app.Database.auth import get_current_user
from app.Database.model import Chat, Message, User
router=APIRouter()

@router.get("/myworkspace")
def get_documentList(
    user: User = Depends(get_current_user)
):
    vectorstore = get_vectorstore()

    documents = vectorstore.get(
        where={"user_id": user.id}
    )

    metadatas = documents["metadatas"]

    sources = {meta.get("source") for meta in metadatas if meta.get("source")}

    print("Sources:", sources)

    return {"sources": list(sources)} 

@router.delete("/delete_source/{sourceName}")
def deleteSource(
    sourceName:str,
    user:User=Depends(get_current_user)
):
    vectorstore=get_vectorstore()
    vectorstore.delete(
        where={
            "$and": [
                {"user_id": user.id},
                {"source": sourceName}
            ]
        }
    )
    return {"message" : "All documents deleted for {sourceName}"}

