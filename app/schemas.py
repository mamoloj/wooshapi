from datetime import datetime
from os import access
from turtle import title
from typing import Optional
from pydantic import BaseModel , EmailStr




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #set a default value to true if not entered , it is also optional field
    #rating: Optional[int] = None #make sure to import Optional from typing and Option is use if we want to set to allow none or int  

class PostCreate(PostBase):
    pass



class UsersResponse(BaseModel):
    id: int
    last_login: Optional[datetime] = None
    first_name: str
    last_name: str
    email:str
    is_verified: bool
    is_deleted: bool
    date_joined: datetime

    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True


class WooshieUsersResponse(BaseModel):

    name : Optional[str]
    organization_name : Optional[str]
    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True



class WooshieScoresResponse(BaseModel):

    name : Optional[str]
    email : str
    score : Optional[int]
    total_score_today : Optional[int]
    description : str
    created_date : datetime
    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True


class WooshieExerciseResponse(BaseModel):

    name : str
    title : str
    description : str
    plan : str
    start_date : datetime
    day : int
    is_done : bool
    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True



class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    #is class is use to allow orm type response not just dict type 
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
