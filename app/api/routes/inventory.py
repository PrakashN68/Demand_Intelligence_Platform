from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse
)
from app.services.inventory_service import (
    create_inventory,
    get_all_inventory
)




router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post(
    "/",
    response_model=InventoryResponse
)
def add_inventory(
        inventory: InventoryCreate,
        db: Session = Depends(get_db)
):

    return create_inventory(db, inventory)


@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def list_inventory(
        db: Session = Depends(get_db)
):

    return get_all_inventory(db)