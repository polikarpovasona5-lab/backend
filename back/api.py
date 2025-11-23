from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from services import UserService, PostService
from schemas import UserCreate, UserResponse, UserUpdate, PostCreate, PostResponse

router = APIRouter()

# POST /users/ - создать пользователя
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)

# GET /users/{user_id} - данные пользователя
@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)

# PATCH /users/{user_id} - обновить пользователя
@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, user)

# POST /posts/ - создать пост от текущего пользователя
@router.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return PostService.create_post(db, post)

# GET /posts/ - все посты текущего пользователя
@router.get("/posts/", response_model=List[PostResponse])
def read_posts(limit: Optional[int] = None, db: Session = Depends(get_db)):
    return PostService.get_user_posts(db, limit)