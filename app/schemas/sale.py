from datetime import datetime

from pydantic import BaseModel


class SaleCreate(BaseModel):
    product_id: int
    store_id: int
    quantity: int


class SaleResponse(SaleCreate):
    id: int
    sale_time: datetime

    class Config:
        from_attributes = True
        