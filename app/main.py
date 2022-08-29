from multiprocessing.sharedctypes import synchronized
from os import stat
from pstats import Stats
from random import randrange
from turtle import pos, title
from typing import Optional , List
from urllib import response
from fastapi import FastAPI, Response , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel 
from urllib3 import Retry #helps us to validate data
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas , utils , oauth2
from .database import engine , get_db
from sqlalchemy.orm import Session
from .routers import user , post , auth , woosh5
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


# models.Base.metadata.create_all(bind=engine)
#uvicorn --host 0.0.0.0 app.main:app 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["get"],
    allow_headers=["*"],
)


while True :
    try:
        conn = psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error :
        print("connecting to database failed")
        print("Error : ", error)
        time.sleep(2)
    


# app.include_router(post.router)

# app.include_router(user.router)

app.include_router(woosh5.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message" : "test"}


