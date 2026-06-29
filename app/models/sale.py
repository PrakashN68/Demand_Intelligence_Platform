from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.db.base import Base


class Sale(Base):
    __tablename__ = "sales"

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

    quantity = Column(
        Integer,
        nullable=False
    )

    sale_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Many Sales -> One Product
    product = relationship(
        "Product",
        back_populates="sales"
    )

    # Many Sales -> One Store
    store = relationship(
        "Store",
        back_populates="sales"
    )
    