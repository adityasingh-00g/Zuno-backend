from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.Database.database import SessionLocal
from app.Database.model import User
from sqlalchemy import text
from fastapi.security import OAuth2PasswordBearer
import hashlib
from app.core.config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_db():
    db=SessionLocal()
    print("DB connected successfully\n")
    try:
        print("DB connected successfully\n")
        yield db
    finally:
        db.close()

def hash_password(password: str):
    sha_password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha_password)


def verify_password(password, hashed):
    sha_password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(sha_password, hashed)

def create_token(user_id):
    payload={
        "user_id":user_id,
        "exp":datetime.utcnow() +timedelta(hours=1)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["user_id"]).first()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid user")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
