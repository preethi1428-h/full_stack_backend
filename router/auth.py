from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from modules.models import User
from schemas.schemas import UserRegister, UserLogin, UserResponse




router = APIRouter(prefix="/auth", tags=["User Login"])

 # REGISTER
@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):


    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone, 
        password=user.password

           
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

 
# LOGIN
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login Successful",
        "email": db_user.email,
        "id": db_user.id
    }

