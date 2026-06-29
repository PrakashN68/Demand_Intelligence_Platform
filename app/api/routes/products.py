from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.product import ProductCreate
from app.schemas.product import ProductResponse

from app.services import product_service
from app.core.security import require_role



router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
        current_user=Depends(
            require_role(["admin"])
)):

    return product_service.create_product(db, product)


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
        product_id: int,
        db: Session = Depends(get_db)
):

    product = product_service.get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        db: Session = Depends(get_db)
):

    product = product_service.delete_product(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {"message": "Product deleted successfully"}
