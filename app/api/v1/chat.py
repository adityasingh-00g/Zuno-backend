from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.rag.pipeline import pipeline, GraphState
from app.Database.model import Chat, Message, User
from app.Database.auth import get_db,get_current_user


router=APIRouter()

class ChatRequest(BaseModel):
    query:str
    chat_id:int |  None = None

class ChatResponse(BaseModel):
    chat_id:int
    answer:str

@router.post("/chat",response_model=ChatResponse)
def chat_endpoint(
    payload:ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if not user:
        raise HTTPException(status_code=401,detail="Unothorized Access !")
    
    if payload.chat_id:
        chat=db.query(Chat).filter(
            Chat.id==payload.chat_id,
            Chat.user_id==user.id
        ).first()

        if not chat:
            raise HTTPException(status_code=404,detail="Chat not found !")
    else:
        chat=Chat(
            user_id=user.id,
            title=payload.query[:40]
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
    
    db.add(
        Message(
            chat_id=chat.id,
            role="user",
            content=payload.query
        )
    )
    db.commit()

    max_hit=6
    hit=0
    last_value=None

    app=pipeline(GraphState)
    input={
        "question":payload.query,
        "user_id":user.id
    }

    for output in app.stream(input):
        hit+=1
        for _,value in output.items():
            last_value=value
        if(hit >= max_hit):
            break
    if(hit>=max_hit):
        answer = "I couldn’t find enough information to answer this properly. Try being more specific or include relevant details."
    else:
        answer=last_value["generation"]
    
    db.add(
        Message(
            chat_id=chat.id,
            role="bot",
            content=answer
        )
    )
    db.commit()

    return {
        "chat_id":chat.id,
        "answer":answer
    }