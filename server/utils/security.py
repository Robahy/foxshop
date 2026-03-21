from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str, plain_password:str) -> bool:
    return pwd_context.verify(password, plain_password)