from pydantic import BaseModel

class SignupSchema(BaseModel):
    email:str
    password:str

class LoginSchema(BaseModel):
    email:str
    password:str

class ChatSchema(BaseModel):
    message:str
    chat_id:int | None