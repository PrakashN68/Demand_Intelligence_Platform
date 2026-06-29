from contextlib import asynccontextmanager # 1. Import context manager
from fastapi import FastAPI

from app.db.init_db import init_db
from app.api.routes.products import router as product_router
from app.api.routes.stores import router as store_router
from app.api.routes.sales import router as sale_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.daily_demand_summary import router as demand_summary_router
from app.api.routes.forecasts import router as forecast
from app.api.routes.inventory import router as inventory
from app.api.routes.replenishment import router as replenishment
from app.core.security import hash_password
from app.api.routes.user import router as user



print(hash_password("admin123"))
# 2. Define the lifespan function to handle startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs ON STARTUP
    init_db()
    yield
    # Any code written after 'yield' would run ON SHUTDOWN

# 3. Pass the lifespan to your FastAPI instance
app = FastAPI(
    title="Demand Intelligence Platform",
    lifespan=lifespan 
)

# 4. Mount your product routes
app.include_router(product_router)
app.include_router(store_router)
app.include_router(sale_router)
app.include_router(analytics_router)
app.include_router(demand_summary_router)
app.include_router(forecast)
app.include_router(inventory)
app.include_router(replenishment)
app.include_router(user)

@app.get("/")
def health_check():
    return {
        "status": "running"
    }
