from sqlalchemy.orm import  Session
from model import User
from schema import UserSchema
from fastapi import  HTTPException
from passlib.context import CryptContext
# from passlib.hash import bcrypt
from datetime import datetime, timedelta
import passlib
import jwt
pwt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "1234"


def create_user(db:Session, user:UserSchema):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwt_context.hash(user.password)
    # hashed_password = bcrypt.hash(user.password)
    _user = User(username=user.username,password=hashed_password)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def login(db:Session, user:UserSchema):
    _user = db.query(User).filter(User.username == user.username).first()
    if not _user:
        raise HTTPException(status_code=401, detail="Invalid username or pssword")
    # verify pssword
    hashed_pass = _user.password
    password=user.password
    is_valid = pwt_context.verify(password, hashed_pass)

    if is_valid:
        print("The password is valid.")
    else:
        print("The password is invalid.")
    if not pwt_context.verify(password, hashed_pass):
        raise HTTPException(status_code=401, detail="Invalid username or pssword")
    token  = generate_token(user.username)
    return {"acess_token":token }


def generate_token(username:str):
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":username, "exp":expiry}
    token  = jwt.encode(payload,SECRET_KEY,algorithm="HS256")
    return token
