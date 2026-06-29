from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, unique=True)

    name = Column(String)

    category = Column(String)

    # One Product -> Many Sales
    sales = relationship("Sale",back_populates="product")

    