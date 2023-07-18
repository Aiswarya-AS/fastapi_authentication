from sqlalchemy.orm import  Session
from model import User
from schema import UserSchema
from fastapi import  HTTPException
from passlib.context import CryptContext

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserSchema):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwt_context.hash(user.password)
    _user = User(username=user.username,password=hashed_password)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user