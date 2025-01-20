from sqlalchemy import Column, ForeignKey, DECIMAL, Index, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.models.enums import PaymentType
from src.models.base import BaseModel


class Check(BaseModel):
    __tablename__ = "checks"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="checks")
    products = relationship("Product", back_populates="check", lazy="joined")
    payment = relationship("Payment", back_populates="check", uselist=False, lazy="joined")
    total_price = Column(DECIMAL(precision=10, scale=2), nullable=False, index=True)

    __table_args__ = (
        Index('ix_check_created_at', 'created_at'),
    )

