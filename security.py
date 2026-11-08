import os
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User

SECRET = os.environ.get('JWT_SECRET', 'DEV_ONLY_CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT')
ALGORITHM = 'HS256'
password_hash = PasswordHash.recommended()
bearer = HTTPBearer()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def token_for(user_id: int) -> str:
    return jwt.encode({'sub': str(user_id), 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, SECRET, algorithm=ALGORITHM)

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=[ALGORITHM])
        user = db.get(User, int(payload['sub']))
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        user = None
    if user is None:
        raise HTTPException(401, 'Invalid or expired token')
    return user
