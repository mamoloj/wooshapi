from base64 import encode
from msilib import schema
from fastapi import Depends , status , HTTPException
from jose import JWTError , jwt
from datetime import datetime , timedelta

from urllib3 import Retry
from . import schemas
from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str , credentials_exception):
    try :    
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        token_id : str = payload.get("user_id")

        if not token_id :
            raise credentials_exception
        token_data = schemas.TokenData(id = token_id)

    except JWTError:
        raise credentials_exception
    return token_data



def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials" ,headers={"WWW-Authenticate" : "Bearer"})
    print(token)
    print(credentials_exception)
    return verify_access_token(token,credentials_exception)