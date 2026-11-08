from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import User, Follow
from schemas import UserOut, PublicUser, ProfileUpdate
from security import current_user

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/me', response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

@router.patch('/me', response_model=UserOut)
def update_me(data: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{user_id}', response_model=PublicUser)
def profile(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, 'User not found')
    return user

@router.post('/{user_id}/follow')
def toggle_follow(user_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if user.id == user_id:
        raise HTTPException(400, 'Cannot follow yourself')
    if not db.get(User, user_id):
        raise HTTPException(404, 'User not found')
    relation = db.scalar(select(Follow).where(Follow.follower_id == user.id, Follow.following_id == user_id))
    if relation:
        db.delete(relation)
        following = False
    else:
        db.add(Follow(follower_id=user.id, following_id=user_id))
        following = True
    db.commit()
    return {'following': following}
