from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.database import get_db
from app import models
from app.schemas import UserCreate, UserLogin
from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_pw = hash_password(
        user.password
    )

    new_user = models.User(
        username=user.username,
        password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User Created"
    }

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid = verify_password(
        user.password,
        db_user.password
    )

    if not valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        data={
            "user_id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }