from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.store import (
    StoreCreate,
    StoreResponse
)
from app.services import store_service

router = APIRouter(
    prefix="/stores",
    tags=["Stores"]
)


@router.post("/", response_model=StoreResponse)
def create_store(
    store: StoreCreate,
    db: Session = Depends(get_db)
):
    return store_service.create_store(db, store)


@router.get("/", response_model=list[StoreResponse])
def get_stores(
    db: Session = Depends(get_db)
):
    return store_service.get_all_stores(db)


@router.get("/{store_id}",
            response_model=StoreResponse)
def get_store(
    store_id: int,
    db: Session = Depends(get_db)
):

    store = store_service.get_store_by_id(
        db,
        store_id
    )

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    return store


@router.delete("/{store_id}")
def delete_store(
    store_id: int,
    db: Session = Depends(get_db)
):

    store = store_service.delete_store(
        db,
        store_id
    )

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    return {
        "message": "Store deleted successfully"
    }

