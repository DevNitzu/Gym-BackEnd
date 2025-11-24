from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user_id: int, user_type: str, expires_delta: timedelta = None):
    to_encode = {
        "sub": str(user_id),   # ID del usuario
        "type": user_type,     # "cliente" o "empleado"
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)



def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print("Decoded Payload:", payload)
        return payload
    except JWTError:
        return None