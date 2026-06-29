from pydantic import BaseModel


class StoreCreate(BaseModel):
    name: str
    city: str
    state: str


class StoreResponse(StoreCreate):
    id: int

    class Config:
        from_attributes = True