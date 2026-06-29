from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    city = Column(String, nullable=False)

    state = Column(String, nullable=False)

    # One Store -> Many Sales
    sales = relationship(
        "Sale",
        back_populates="store"
    )
    