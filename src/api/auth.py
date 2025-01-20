from datetime import timedelta

from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import db_helper
from src.errors import UnauthorizedError
from src.schemas import UserCreate, TokenResponse
from src.services.user_service import authenticate_user, register_user_service
from src.utils.auth import create_access_token

router = APIRouter()


@router.post(
    "/register",
    summary="Register new user",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    await register_user_service(user_data, db)
    return {"msg": "User successfully registered"}


@router.post(
    "/token",
    summary="Authenticate user and provide access token",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise UnauthorizedError
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=expires)
    return TokenResponse(access_token=access_token, token_type="bearer")
