from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

