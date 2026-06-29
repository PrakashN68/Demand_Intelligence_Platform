from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.replenishment_service import (
    get_replenishment_recommendation
)

router = APIRouter(
    prefix="/replenishment",
    tags=["Replenishment"]
)


@router.get("/{product_id}/{store_id}")
def get_recommendation(
        product_id: int,
        store_id: int,
        db: Session = Depends(get_db)
):

    return get_replenishment_recommendation(
        db=db,
        product_id=product_id,
        store_id=store_id
    )
