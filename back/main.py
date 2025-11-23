from fastapi import FastAPI, Depends        
from sqlalchemy.orm import Session
from typing import List

from api import router                         
from database import get_db

app = FastAPI()                                

app.include_router(router)                    
