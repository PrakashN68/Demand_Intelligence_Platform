from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse
)
from app.services.user_service import create_user
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import Token
from app.services.user_service import authenticate_user
from app.core.security import create_access_token



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse
)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    return create_user(
        db=db,
        user=user
    )

@router.post(
    "/login",
    response_model=Token
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
