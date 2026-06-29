from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.sale import (
    SaleCreate,
    SaleResponse
)

from app.services import sale_service



router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):

    db_sale, error = sale_service.create_sale(
        db,
        sale
    )

    if error:
        raise HTTPException(
            status_code=404,
            detail=error
        )

    return db_sale


@router.get("/", response_model=list[SaleResponse])
def get_sales(
    db: Session = Depends(get_db)
):
    return sale_service.get_all_sales(db)


@router.get("/{sale_id}",
            response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):

    sale = sale_service.get_sale_by_id(
        db,
        sale_id
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):

    sale = sale_service.delete_sale(
        db,
        sale_id
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return {
        "message": "Sale deleted successfully"
    }