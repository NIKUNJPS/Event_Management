from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError
from app.database import get_db, next_id
from app.schemas import RegisterIn, LoginIn, TokenOut
from app.services.auth import hash_password, verify_password, create_token
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenOut)
def register(data: RegisterIn, db=Depends(get_db)):
    if db.users.find_one({"email": data.email}): raise HTTPException(409, "Email already registered")
    user = {"_id": next_id(db, "users"), "name": data.name, "email": data.email, "password_hash": hash_password(data.password), "role": "user"}
    try: db.users.insert_one(user)
    except DuplicateKeyError: raise HTTPException(409, "Email already registered")
    return {"access_token": create_token(user["_id"], user["role"])}

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db=Depends(get_db)):
    user = db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password_hash"]): raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user["_id"], user["role"])}
