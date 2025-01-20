from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    check_id = Column(UUID(as_uuid=True), ForeignKey("checks.id"), nullable=False)
    check = relationship("Check", back_populates="products")

    name = Column(String, nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    total_price = Column(Numeric(precision=10, scale=2), nullable=False)



