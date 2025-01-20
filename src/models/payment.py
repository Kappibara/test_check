from sqlalchemy import Column, ForeignKey, Enum, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.enums import PaymentType
from src.models.base import BaseModel


class Payment(BaseModel):
    __tablename__ = "payments"

    type = Column(Enum(PaymentType), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    check_id = Column(UUID(as_uuid=True), ForeignKey("checks.id"), nullable=False)
    check = relationship("Check", back_populates="payment")
