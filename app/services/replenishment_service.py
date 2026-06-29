from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.services.forecast_service import (
    get_moving_average_forecast
)



def get_replenishment_recommendation(
        db: Session,
        product_id: int,
        store_id: int
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id,
            Inventory.store_id == store_id
        )
        .first()
    )

    if not inventory:
        return {
            "message": "Inventory not found"
        }

    forecast = get_moving_average_forecast(
        db=db,
        product_id=product_id
    )

    SAFETY_STOCK = 20

    recommended_qty = max(
        0,
        forecast + SAFETY_STOCK
        - inventory.stock_on_hand
    )

    return {
        "product_id": product_id,
        "store_id": store_id,
        "current_stock": inventory.stock_on_hand,
        "forecast_demand": forecast,
        "safety_stock": SAFETY_STOCK,
        "recommended_order_quantity": round(
            recommended_qty
        )
    }

