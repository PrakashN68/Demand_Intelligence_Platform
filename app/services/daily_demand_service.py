from datetime import date

from sqlalchemy.orm import Session

from app.models.daily_demand_summary import DailyDemandSummary


def update_daily_demand_summary(db: Session, quantity: int):

    today = date.today()

    summary = (
        db.query(DailyDemandSummary)
        .filter(DailyDemandSummary.date == today)
        .first()
    )

    # Row already exists
    if summary:
        summary.total_quantity += quantity

    # First sale of the day
    else:
        summary = DailyDemandSummary(
            date=today,
            total_quantity=quantity
        )

        db.add(summary)

    db.commit()

def get_daily_demand_summary(db: Session):
    return db.query(DailyDemandSummary).all()

