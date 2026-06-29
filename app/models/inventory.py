from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    store_id = Column(
        Integer,
        ForeignKey("stores.id"),
        nullable=False
    )

    stock_on_hand = Column(
        Integer,
        nullable=False
    )

    reorder_point = Column(
        Integer,
        nullable=False
    )

    product = relationship("Product")

    store = relationship("Store")
