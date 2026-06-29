from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.daily_demand_service import get_daily_demand_summary



router = APIRouter(
    prefix="/daily-demand-summary",
    tags=["Daily Demand Summary"]
)


@router.get("/")
def get_summary(db: Session = Depends(get_db)):
    return get_daily_demand_summary(db)
