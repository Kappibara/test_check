import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import db_helper
from src.errors import UnauthorizedError, UserAlreadyExistsError
from src.models import User
from src.repositories.user_repo import get_user_by_email_repo, create_user_repo
from src.schemas import UserCreate, TokenData
from src.utils.auth import get_password_hash, verify_password


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user_by_email_repo(username, db)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


async def register_user_service(user_data: UserCreate, db: AsyncSession) -> User :
    is_user_exists = await get_user_by_email_repo(user_data.email, db)
    if is_user_exists:
        raise UserAlreadyExistsError
    user_data.password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict['hashed_password'] = user_dict.pop('password')
    created_user = await create_user_repo(user_dict, db)
    return created_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(db_helper.session_getter)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedError
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise UnauthorizedError
    user = await get_user_by_email_repo(token_data.username, db)
    if user is None:
        raise UnauthorizedError
    return user
