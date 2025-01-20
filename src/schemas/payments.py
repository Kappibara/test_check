from decimal import Decimal
from pydantic import BaseModel

from src.models.enums import PaymentType


class Payment(BaseModel):
    type: PaymentType
    amount: Decimal
