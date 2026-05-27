from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import User
from core.auth_service import create_user, authenticate_user
from fastapi import HTTPException
router = APIRouter()


# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(data: dict, db: Session = Depends(get_db)):
    username = data.get("username").strip()
    password = data.get("password").strip()

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    create_user(db, username, password)
    return {"msg": "User created successfully"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    username = data.get("username").strip()
    password = data.get("password").strip()

    user = authenticate_user(db, username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"msg": "Login successful"}


# ---------------- PREDICT ----------------
from core.services.cost_service import full_prediction

@router.post("/predict")
def predict(data: dict):
    return full_prediction(
        data.get("area"),
        data.get("floors"),
        data.get("year")
    )