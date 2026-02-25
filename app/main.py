from fastapi import FastAPI, Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.chat import router as chatRouter
from app.api.v1.documentUpload import router as docUploadRouter
from app.api.v1.workspace import router as workspaceRouter
from app.rag.embeddings import warmup_embeddings
from app.Database.database import engine
from app.Database.model import Base,User, Chat
from app.Database.auth import get_db, hash_password, verify_password, create_token, get_current_user
from app.Database.schema import SignupSchema, LoginSchema
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)
app = FastAPI(title="RAG BACKEND")

@app.on_event("startup")
def startup_event():
    warmup_embeddings()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
def signup(data:SignupSchema,db=Depends(get_db)):
    user=User(
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message":"User created"}

@app.post("/login")
def login(data:LoginSchema,db=Depends(get_db)):
    user=db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credential")
    
    return {"access_token":create_token(user.id)}

@app.get("/fetchallchats")
def get_user_chats(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    chats=(db.query(Chat).filter(Chat.user_id==current_user.id).order_by(Chat.created_at.desc()).all())
    return chats

@app.get("/fetchchat/{chat_id}")
def get_chat_messages(
    chat_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    chat=(db.query(Chat).filter(Chat.id==chat_id,
                               Chat.user_id==current_user.id).first()
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found !")
    return chat.messages


# Include the chat router
app.include_router(chatRouter, prefix="/api/v1")
app.include_router(docUploadRouter,prefix="/api/v1")
app.include_router(workspaceRouter,prefix="/api/v1")


# Optional: Root endpoint for testing
@app.get("/")
def root():
    return {"message": "RAG Backend is running!"}


