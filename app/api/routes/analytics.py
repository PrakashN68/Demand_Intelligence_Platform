from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.services import analytics_service




router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/sales")
def sales_analytics(
        db: Session = Depends(get_db)
):

    return analytics_service.get_sales_analytics(db)

@router.get("/top-products")
def top_products(
        db: Session = Depends(get_db)
):

    return analytics_service.get_top_products(db)

@router.get("/daily-demand")
def daily_demand(
        db: Session = Depends(get_db)
):

    return analytics_service.get_daily_demand(db)

@router.get("/store-performance")
def store_performance(
    db: Session = Depends(get_db)
):

    return analytics_service.get_store_performance(db)

@router.get("/demand-spikes")
def demand_spikes(
    db: Session = Depends(get_db)
):

    return analytics_service.detect_demand_spikes(db)
