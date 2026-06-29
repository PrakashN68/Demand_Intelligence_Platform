from app.db.base import Base
from app.db.database import engine

from app.models.product import Product
from app.models.store import Store
from app.models.sale import Sale
from app.models.daily_demand_summary import DailyDemandSummary
from app.models.inventory import Inventory
from app.models.user import User


def init_db():
    Base.metadata.create_all(bind=engine)

    