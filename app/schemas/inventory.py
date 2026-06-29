from pydantic import BaseModel


class InventoryCreate(BaseModel):
    product_id: int
    store_id: int
    stock_on_hand: int
    reorder_point: int


class InventoryResponse(InventoryCreate):
    id: int

    class Config:
        from_attributes = True