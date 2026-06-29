from sqlalchemy import Column, Integer, Date

from app.db.base import Base


class DailyDemandSummary(Base):

    __tablename__ = "daily_demand_summary"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, unique=True, nullable=False)

    total_quantity = Column(
        Integer,
        default=0
    )
