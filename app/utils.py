from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto") #for password hashing

def hash(password:str):
    return pwd_context.hash(password)

def verify_pass(plain_pass,hash_pass):
    return pwd_context.verify(plain_pass,hash_pass)