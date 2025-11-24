from typing import List, Optional
import json

from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories import UserRepository, PostRepository
from schemas import (
    UserCreate, UserResponse, UserUpdate, PostCreate, PostResponse
)
from models import User, Post


class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        # Проверка возраста
        if user_data.age < 0:
            raise HTTPException(
                status_code=400, detail="Возраст должен быть положительным"
                )
        # Создаем пользователя напрямую (без репозитория)
        hobbies_json = json.dumps(user_data.hobbies)

        db_user = User(
            last_name=user_data.last_name,
            first_name=user_data.first_name,
            patronymic=user_data.patronymic,
            photo_url=user_data.photo_url,
            education_place=user_data.education_place,
            age=user_data.age,
            hobbies=hobbies_json
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Преобразуем hobbies из JSON обратно в список для ответа
        hobbies_list = json.loads(db_user.hobbies)
        
        return UserResponse(
            id=db_user.id,
            last_name=db_user.last_name,
            first_name=db_user.first_name,
            patronymic=db_user.patronymic,
            photo_url=db_user.photo_url,
            education_place=db_user.education_place,
            age=db_user.age,
            hobbies=hobbies_list
        )

    @staticmethod
    def get_user(db: Session, user_id: int) -> UserResponse:
        db_user = UserRepository.get_user_by_id(db, user_id)

        if not db_user:
            raise HTTPException(
                status_code=404, detail="Пользователь не найден"
                )

        hobbies_list = json.loads(db_user.hobbies)

        return UserResponse(
            id=db_user.id,
            last_name=db_user.last_name,
            first_name=db_user.first_name,
            patronymic=db_user.patronymic,
            photo_url=db_user.photo_url,
            education_place=db_user.education_place,
            age=db_user.age,
            hobbies=hobbies_list
        )

    @staticmethod
    def update_user(
        db: Session, user_id: int, user_data: UserUpdate
    ) -> UserResponse:
        # Получаем пользователя через репозиторий
        db_user = UserRepository.get_user_by_id(db, user_id)

        # Если пользователь не найден
        if not db_user:
            raise HTTPException(
                status_code=404, detail="Пользователь не найден"
                )

        # Обновляем только переданные поля
        update_data = user_data.dict(exclude_unset=True)

        if 'hobbies' in update_data:
            update_data['hobbies'] = json.dumps(update_data['hobbies'])

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)

        hobbies_list = json.loads(db_user.hobbies)

        return UserResponse(
            id=db_user.id,
            last_name=db_user.last_name,
            first_name=db_user.first_name,
            patronymic=db_user.patronymic,
            photo_url=db_user.photo_url,
            education_place=db_user.education_place,
            age=db_user.age,
            hobbies=hobbies_list
        )


class PostService:
    # ВРЕМЕННО - будем использовать user_id = 1 как текущего пользователя
    CURRENT_USER_ID = 1

    @staticmethod
    def create_post(db: Session, post_data: PostCreate) -> PostResponse:
        # Проверяем, существует ли пользователь через репозиторий
        user = UserRepository.get_user_by_id(db, PostService.CURRENT_USER_ID)

        # Если пользователь не найден
        if not user:
            raise HTTPException(
                status_code=404, detail="Пользователь не найден"
                )

        # Создаем пост через репозиторий
        db_post = PostRepository.create_post(
            db, post_data, PostService.CURRENT_USER_ID
            )

        return PostResponse(
            id=db_post.id,
            title=db_post.title,
            description=db_post.description,
            created_at=db_post.created_at,
            user_id=db_post.user_id
        )

    @staticmethod
    def get_user_posts(
        db: Session, limit: Optional[int] = None
    ) -> List[PostResponse]:
        # Получаем посты текущего пользователя напрямую (без репозитория)
        from sqlalchemy import select

        query = (
            select(Post)
            .where(Post.user_id == PostService.CURRENT_USER_ID)
            .order_by(Post.created_at.desc())
        )

        if limit:
            query = query.limit(limit)

        result = db.execute(query)
        posts = result.scalars().all()

        posts_response = []
        for post in posts:
            posts_response.append(PostResponse(
                id=post.id,
                title=post.title,
                description=post.description,
                created_at=post.created_at,
                user_id=post.user_id
            ))

        return posts_response
