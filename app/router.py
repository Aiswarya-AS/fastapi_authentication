from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schema import UserSchema, RequestUser, Response
import authentiation

router=APIRouter()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
async def create_user(request:RequestUser, db:Session = Depends(get_db)):
    authentiation.create_user(db, user=request.parameter )
    return Response[str](status="Ok", code='200', message="User Created", result = None).dict(exclude_none=True)

@router.post('/login')
async def login_user(request:RequestUser, db:Session=Depends(get_db)):
    authentiation.login(db, request.parameter)
    return Response[str](status="Ok", code='200', message="User loginned", result = None).dict(exclude_none=True)
    