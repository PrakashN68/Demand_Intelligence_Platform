from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.forecast_service import (
    get_moving_average_forecast
)
from app.core.security import get_current_user


router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.get("/{product_id}")
def forecast_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):

    forecast = get_moving_average_forecast(
        db=db,
        product_id=product_id
    )

    return {
        "product_id": product_id,
        "forecast_quantity": forecast
    }