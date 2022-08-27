from typing import List
from fastapi import  Response , status , HTTPException , Depends , APIRouter
from .. import models , schemas , utils , main , oauth2
from ..database import get_db
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/users",tags=["users"])




# @router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreateResponse) #set status code to 201 if created
# def create_user(new_user:schemas.UserCreate,db: Session = Depends(get_db)):

#     #hash the password 
#     hashed_password =  utils.hash(new_user.password)
#     new_user.password = hashed_password
#     user = models.User(**new_user.dict()) #** is a python operator to unpack dictionaries into other dictionaries
#     db.add(user)
#     db.commit()
#     db.refresh(user) #refresh is to get the data, is need to inorder to view it as a return value
#     return user


# @router.get("/",response_model=List[schemas.UserCreateResponse])
# def get_users(db: Session = Depends(get_db)):
#     print(utils.hash("Mypassword123!"),"password")
#     users = db.query(models.User).all()
#     return users

# @router.get("/{id}",response_model=schemas.UserCreateResponse)
# def get_user(id:int,db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} was not found")
#     return user




# @router.put("/{id}",response_model=schemas.UserCreateResponse)
# def update_user(id:int,updated_user:schemas.UserCreate,db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first() :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} was not found")
#     user.update(updated_user.dict(),synchronize_session=False)
#     db.commit()
#     return user.first()


