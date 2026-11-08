from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import User, Post, Like, Comment
from schemas import PostCreate, PostOut, CommentCreate, CommentOut
from security import current_user

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.post('', response_model=PostOut, status_code=201)
def create_post(data: PostCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    post = Post(user_id=user.id, content=data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get('', response_model=list[PostOut])
def feed(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return db.scalars(select(Post).order_by(Post.created_at.desc(), Post.id.desc()).offset(offset).limit(limit)).all()

@router.delete('/{post_id}')
def delete_post(post_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(404, 'Post not found')
    if post.user_id != user.id:
        raise HTTPException(403, 'Not your post')
    db.query(Like).filter(Like.post_id == post_id).delete()
    db.query(Comment).filter(Comment.post_id == post_id).delete()
    db.delete(post)
    db.commit()
    return {'deleted': True}

@router.post('/{post_id}/like')
def toggle_like(post_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, 'Post not found')
    like = db.scalar(select(Like).where(Like.post_id == post_id, Like.user_id == user.id))
    if like:
        db.delete(like)
        liked = False
    else:
        db.add(Like(post_id=post_id, user_id=user.id))
        liked = True
    db.commit()
    return {'liked': liked}

@router.post('/{post_id}/comments', response_model=CommentOut, status_code=201)
def add_comment(post_id: int, data: CommentCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, 'Post not found')
    comment = Comment(post_id=post_id, user_id=user.id, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get('/{post_id}/comments', response_model=list[CommentOut])
def comments(post_id: int, db: Session = Depends(get_db)):
    if not db.get(Post, post_id):
        raise HTTPException(404, 'Post not found')
    return db.scalars(select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at)).all()
