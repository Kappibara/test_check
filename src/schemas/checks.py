import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.schemas.payments import Payment
from src.schemas.products import Product


class CheckCreate(BaseModel):
    products: List[Product]
    payment: Payment

    class Config:
        from_attributes = True


class CheckResponse(BaseModel):
    id: uuid.UUID
    products: List[Product]
    payment: Payment
    created_at: datetime
    updated_at: datetime
    total_price: float

    class Config:
        from_attributes = True


class CheckText(BaseModel):
    id: uuid.UUID
    text: str

    class Config:
        from_attributes = True
