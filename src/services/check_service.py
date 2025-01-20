from decimal import Decimal
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.check import CheckFilter
from src.models import Check, Product, Payment
from src.schemas import (
    CheckCreate,
)


async def create_check_service(check_data: CheckCreate, db: AsyncSession,  user_id: UUID) -> Check:
    check = Check(user_id=user_id)
    model_products = []
    total_price = Decimal(0)
    for product in check_data.products:
        total_price += product.total
        model_products.append(Product(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            total_price=product.total,
            check=check # noqa
        ))

    payment_data = check_data.payment
    payment = Payment(
        type=payment_data.type.value,
        amount=payment_data.amount,
        check=check # noqa
    )

    check.products = model_products
    check.payment = payment
    check.total_price = total_price

    db.add(check)
    await db.commit()
    await db.refresh(check)
    return check




async def get_checks(check_filter: CheckFilter, db: AsyncSession, user_id: UUID):
    query = check_filter.filter(
        select(Check).join(Payment).where(Check.user_id == user_id).order_by(Check.created_at)
    )
    return await paginate(db, query)


async def get_check(check_id: UUID, db: AsyncSession):
    query = (
        select(Check)
        .where(Check.id == check_id)
    )
    result = await db.execute(query)
    check = result.unique().scalar_one()
    return check