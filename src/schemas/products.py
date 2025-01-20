from decimal import Decimal

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str = ""
    price: Decimal
    quantity: float

    class Config:
        from_attributes = True

    @property
    def total(self) -> Decimal:
        return self.price * Decimal(str(self.quantity))