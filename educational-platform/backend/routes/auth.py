from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel

from database import get_db
from models import User
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def hash_password(password: str) -> str:
    # Hash a password using bcrypt for secure storage.
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify if a plain password matches its hashed version.
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(email: str) -> str:
    # Create a JWT token for authenticated user.
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str) -> str:
    # Verify JWT token and return email. Raises exception if invalid or expired.
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("email")
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Register a new user with email and password.
    # Returns success message or error if email already exists.
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail={"error": "Email already registered"})
    
    # Hash password and create user
    hashed_password = hash_password(request.password)
    user = User(email=request.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    
    return {"message": "User registered successfully"}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Authenticate user and return JWT token.
    # Returns error if email not found or password is incorrect.
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail={"error": "User not found"})
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail={"error": "Incorrect password"})
    
    # Create and return token
    token = create_jwt_token(user.email)
    return {"token": token}
