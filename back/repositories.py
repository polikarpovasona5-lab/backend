from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
import json

from models import User, Post
from schemas import PostCreate  # ← ТОЛЬКО PostCreate!

class UserRepository:
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Найти пользователя по ID"""
        result = db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

class PostRepository:
    
    @staticmethod
    def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
        """Создать новый пост"""
        db_post = Post(
            title=post.title,
            description=post.description,
            user_id=user_id
        )
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post