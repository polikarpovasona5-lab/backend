from pydantic import BaseModel  
from typing import Optional, List
from datetime import datetime


class Base(BaseModel):
    pass

class UserCreate(Base):
    last_name: str
    first_name: str 
    patronymic: str
    photo_url: Optional[str] = None
    education_place: str
    age: int
    hobbies: List[str]  # Список хобби

class UserResponse(Base):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    photo_url: Optional[str] = None
    education_place: str
    age: int
    hobbies: List[str]

class UserUpdate(Base):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    photo_url: Optional[str] = None
    education_place: Optional[str] = None
    age: Optional[int] = None
    hobbies: Optional[List[str]] = None


class PostCreate(Base):
    title: str
    description: str

class PostResponse(Base):
    id: int
    title: str
    description: str
    created_at: datetime
    user_id: int