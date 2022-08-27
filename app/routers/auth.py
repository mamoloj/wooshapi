from os import access
import token
from fastapi import APIRouter , Depends , status , HTTPException , Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas , models , utils , oauth2
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
conn = psycopg2.connect(host="localhost",database="production",user="postgres",password="password",cursor_factory=RealDictCursor)
cursor = conn.cursor()


router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #for OAuth2PasswordRequestForm form always use username instead email = user_creds.username
    print(user_creds.username)
    #user = db.query(models.AccountsUser).filter(models.AccountsUser.email == user_creds.username).first()
    cursor.execute("select id , name , password from accounts_user where email = %s LIMIT 1",(str(user_creds.username),))
    user = cursor.fetchone()
    conn.commit()
    if not user :
        print("no user")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credetials")
    if not utils.verify_pass(user_creds.password,"$2b$12$yNEVfzM2e7H51FF.4UN/D.QV0lRry/WuvCjLERtFKAdBey3t9/Zzi"):
        print("invalid cred")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credetials")

    access_token = oauth2.create_access_token(data = { "user_id" : user['id'] })

    return {"access_token" : access_token , "token_type" : "bearer"}