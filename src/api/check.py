from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Depends, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.errors import CheckNotFoundError, CheckCreationError, InternalServerError
from src.filters.check import CheckFilter
from src.models import Check
from src.models import User
from src.schemas import (
    CheckCreate,
    CheckResponse,
    CheckText,
)
from src.services import check_service
from src.services.user_service import get_current_user
from src.utils.check import create_formatted_check

router = APIRouter()


@router.post(
    "",
    summary="Create new check",
    status_code=status.HTTP_201_CREATED,
    response_model=CheckResponse,
)
async def create_check(
    data: CheckCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
):
    try:
        new_check = await check_service.create_check_service(data, db, current_user.id)
        return  new_check
    except Exception:
        raise CheckCreationError


@router.get(
    "",
    summary="Get user's checks",
    status_code=status.HTTP_200_OK,
    response_model=Page[CheckResponse],
)
async def get_checks(
    check_filter: CheckFilter = FilterDepends(CheckFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user),
) -> Page[Check]:
    return await check_service.get_checks(check_filter, db, current_user.id)


@router.get(
    "/{check_id}",
    summary="Get text check",
    status_code=status.HTTP_200_OK,
    response_model=CheckText,
)
async def get_formatted_check(
    check_id: UUID,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        check = await check_service.get_check(check_id, db)
    except NoResultFound:
        raise CheckNotFoundError
    except IntegrityError:
        raise InternalServerError

    check_str = create_formatted_check(check)
    return CheckText(id=check.id, text=check_str)
