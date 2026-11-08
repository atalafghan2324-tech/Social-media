from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import Register, Login, UserOut
from security import hash_password, verify_password, token_for

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/register', response_model=UserOut, status_code=201)
def register(data: Register, db: Session = Depends(get_db)):
    if db.scalar(select(User).where((User.email == data.email) | (User.username == data.username))):
        raise HTTPException(409, 'Email or username already registered')
    user = User(username=data.username, email=data.email, full_name=data.full_name, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login')
def login(data: Login, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, 'Invalid credentials')
    return {'access_token': token_for(user.id), 'token_type': 'bearer'}
