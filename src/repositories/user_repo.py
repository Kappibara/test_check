from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import User


async def get_user_by_email_repo(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user_repo(user_data: dict, db: AsyncSession):
    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
