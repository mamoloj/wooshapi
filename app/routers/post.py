
from typing import List
from fastapi import  Response , status , HTTPException , Depends , APIRouter

from app import oauth2
from .. import models , schemas , oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts",tags=["posts"])

#we need to set the reponse model as List[] since we are returning a queryset not just 1 value
@router.get("/") 
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) #set status code to 201 if created
def create_post(new_post:schemas.PostCreate,db: Session = Depends(get_db), current_user_id : int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     "insert into posts (title,content,published)values(%s,%s,%s) RETURNING *",
    #     (new_post.title,new_post.content,new_post.published)
    # )
    # data = cursor.fetchone()
    # conn.commit()
    print(current_user_id)
    data = models.Post(**new_post.dict()) #** is a python operator to unpack dictionaries into other dictionaries
    db.add(data)
    db.commit()
    db.refresh(data) #refresh is to get the data, is need to inorder to view it as a return value
    return data

#if we put this below the get_post it will get an error since it will already consider int 
@router.get("/latest")
def get_latest_post():
    post = None
    return {"post detail": "test"}

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id : int,db: Session = Depends(get_db)): #the :int validate to int
    # cursor.execute("select * from posts where id = %s",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) #for deleting set status code to 204
def delete_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute("delete from posts where id = %s returning *",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id==id)
    if not deleted_post.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db)):

    # cursor.execute("update posts set title = %s, content = %s, published = %s where id = %s returning *",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    #conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exis")
    updated_post.update(post.dict(),synchronize_session=False)
    db.commit()


    return updated_post.first()

