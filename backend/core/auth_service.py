from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.models import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_user(db: Session, username: str, password: str):
    hashed = hash_password(password)
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    print("INPUT PASSWORD:", password)
    print("HASH IN DB:", user.password if user else None)

    if not user:
        print("User not found")
        return None

    if not verify_password(password, user.password):
        print("Password mismatch ❌")
        return None

    print("Login success ✅")
    return user