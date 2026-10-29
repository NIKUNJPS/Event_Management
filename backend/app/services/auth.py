import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)

def hash_password(password): return pwd.hash(password)
def verify_password(password, hashed): return pwd.verify(password, hashed)
def create_token(user_id, role):
    payload = {"sub": str(user_id), "role": role, "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials: raise HTTPException(status_code=401, detail="Authentication required")
    try: payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]); uid = int(payload["sub"])
    except (JWTError, ValueError, KeyError): raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(User, uid)
    if not user: raise HTTPException(status_code=401, detail="User not found")
    return user

def admin_user(user=Depends(current_user)):
    if user.role != "admin": raise HTTPException(status_code=403, detail="Admin access required")
    return user
