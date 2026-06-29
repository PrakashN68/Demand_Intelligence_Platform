from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.sale import Sale
import json
from app.core.redis_client import redis_client


def get_moving_average_forecast(
        db: Session,
        product_id: int
):
    cache_key = f"forecast:{product_id}"

    # Check cache first
    cached_forecast = redis_client.get(cache_key)

    if cached_forecast:
        print("Forecast returned from Redis cache")
        return json.loads(cached_forecast)

    # Aggregate demand by day
    daily_sales = (
        db.query(
            func.date(Sale.sale_time).label("sale_date"),
            func.sum(Sale.quantity).label("daily_quantity")
        )
        .filter(Sale.product_id == product_id)
        .group_by(func.date(Sale.sale_time))
        .order_by(func.date(Sale.sale_time).desc())
        .limit(3)
        .all()
    )

    if not daily_sales:
        forecast = 0
    else:
        quantities = [
            row.daily_quantity
            for row in daily_sales
        ]

        forecast = round(
            sum(quantities) / len(quantities),
            2
        )

    # Store in Redis for 5 minutes
    redis_client.setex(
        cache_key,
        300,
        json.dumps(forecast)
    )

    print("Forecast stored in Redis")

    return forecast