from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.Database.database import Base

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True)
    email=Column(String(255),unique=True,index=True)
    password_hash=Column(String(255))
    created_at=Column(DateTime,default=datetime.utcnow)

    chats=relationship("Chat",back_populates="user",cascade="all,delete")

class Chat(Base):
    __tablename__="chats"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    title=Column(String(255))
    created_at=Column(DateTime,default=datetime.utcnow)
    user=relationship("User",back_populates="chats")
    messages=relationship("Message",back_populates="chat",cascade="all,delete")

class Message(Base):
    __tablename__="messages"

    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer,ForeignKey("chats.id",ondelete="CASCADE"))
    role=Column(String(255))
    content=Column(Text)
    timestamps=Column(DateTime,default=datetime.utcnow)

    chat=relationship("Chat",back_populates="messages")