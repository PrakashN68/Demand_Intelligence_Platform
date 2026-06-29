from sqlalchemy.orm import Session, joinedload
from app.models.sale import Sale
from sqlalchemy import func
from app.models.product import Product
from app.models.store import Store





def get_sales_analytics(db: Session):
    # Fix: Use joinedload to bring in product and store tables in 1 database trip
    sales = db.query(Sale).options(
        joinedload(Sale.product),
        joinedload(Sale.store)
    ).all()

    analytics = []

    for sale in sales:
        analytics.append({
            "sale_id": sale.id,
            "product_name": sale.product.name,  # Already loaded in memory!
            "store_name": sale.store.name,      # Already loaded in memory!
            "quantity": sale.quantity,
            "sale_time": sale.sale_time
        })

    return analytics

def get_top_products(db: Session):

    results = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label(
                "total_quantity_sold"
            )
        )
        .join(Sale, Product.id == Sale.product_id)
        .group_by(Product.name)
        .order_by(
            func.sum(Sale.quantity).desc()
        )
        .all()
    )

    analytics = []

    for product_name, total_quantity in results:

        analytics.append({
            "product_name": product_name,
            "total_quantity_sold": total_quantity
        })

    return analytics

def get_daily_demand(db: Session):

    results = (
        db.query(
            func.date(Sale.sale_time).label("date"),
            func.sum(Sale.quantity).label(
                "total_quantity_sold"
            )
        )
        .group_by(
            func.date(Sale.sale_time)
        )
        .order_by(
            func.date(Sale.sale_time)
        )
        .all()
    )

    analytics = []

    for date, total_quantity in results:

        analytics.append({
            "date": date,
            "total_quantity_sold": total_quantity
        })

    return analytics

def get_store_performance(db: Session):

    results = (
        db.query(
            Store.name,
            func.sum(Sale.quantity).label(
                "total_quantity_sold"
            )
        )
        .join(
            Sale,
            Store.id == Sale.store_id
        )
        .group_by(Store.name)
        .order_by(
            func.sum(Sale.quantity).desc()
        )
        .all()
    )

    analytics = []

    for store_name, total_quantity in results:

        analytics.append({
            "store_name": store_name,
            "total_quantity_sold": total_quantity
        })

    return analytics
def detect_demand_spikes(db: Session):

    # Reuse our daily demand query
    daily_demand = get_daily_demand(db)

    spikes = []

    # Start from second day because first day
    # has no previous day for comparison
    for i in range(1, len(daily_demand)):

        today = daily_demand[i]
        yesterday = daily_demand[i - 1]

        today_qty = today["total_quantity_sold"]
        yesterday_qty = yesterday["total_quantity_sold"]

        # Avoid division by zero
        if yesterday_qty == 0:
            continue

        percentage_increase = (
            (today_qty - yesterday_qty)
            / yesterday_qty
        ) * 100

        if percentage_increase > 50:

            spikes.append({
                "date": today["date"],
                "demand": today_qty,
                "percentage_increase": round(
                    percentage_increase,
                    2
                ),
                "spike_detected": True
            })

    return spikes

