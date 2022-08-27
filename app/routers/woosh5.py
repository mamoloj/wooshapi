from typing import List
from fastapi import  Response , status , HTTPException , Depends , APIRouter 
from .. import models , schemas , utils , main , oauth2
from ..database import get_db
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
router = APIRouter(prefix="/woosh5",tags=["woosh5"])


security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"Admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"Mypassword123!"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



@router.get("/users",response_model=List[schemas.WooshieUsersResponse]) 
def get_wooshie_user(db: Session = Depends(get_db)):
#def get_wooshie_user(db: Session = Depends(get_db), current_user : str = Depends(get_current_username)):
    main.cursor.execute("""
        select u.name as name , org.organization_name as organization_name from accounts_user as u
        left join accounts_organization as org ON org.id = u.organizaion_id;
    """)
    users  = main.cursor.fetchall()
    return  users


@router.get("/scores",response_model=List[schemas.WooshieScoresResponse]) 
def get_wooshie_score(db: Session = Depends(get_db)):
    main.cursor.execute("""
        select  u.name as name , u.email as email , wh.score as score, uwh.score as total_score_today ,  wh.description as description, created_date as created_date  from accounts_userwooshiehistory wh
        left join accounts_user u ON u.id = wh.user_id 
        left join accounts_userwooshie uwh ON uwh.id = wh.wooshie_id
        order by created_date;
    """)
    scores  = main.cursor.fetchall()
    return  scores


@router.get("/exercises",response_model=List[schemas.WooshieExerciseResponse]) 
def get_wooshie_exercise(db: Session = Depends(get_db)):
#def get_wooshie_user(db: Session = Depends(get_db), current_user_id : int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""
        select u.name as name , x.title as title , x.description as description, pl.name as plan , ux.start_date as start_date , ux.day as day, ux.is_done as is_done from exercise_userexercise ux 
        left join accounts_user u ON u.id = ux.user_id
        left join exercise_exercise x ON x.id = ux.exercise_id
        left join goal_plan pl ON pl.id = ux.plan_id;
    """)
    exercise  = main.cursor.fetchall()
    return  exercise