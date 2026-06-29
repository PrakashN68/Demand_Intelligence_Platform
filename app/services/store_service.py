from sqlalchemy.orm import Session

from app.models.store import Store
from app.schemas.store import StoreCreate


def create_store(db: Session, store: StoreCreate):

    db_store = Store(
        name=store.name,
        city=store.city,
        state=store.state
    )

    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store


def get_all_stores(db: Session):
    return db.query(Store).all()


def get_store_by_id(db: Session, store_id: int):
    return db.query(Store).filter(
        Store.id == store_id
    ).first()


def delete_store(db: Session, store_id: int):

    store = get_store_by_id(db, store_id)

    if not store:
        return None

    db.delete(store)
    db.commit()

    return store
