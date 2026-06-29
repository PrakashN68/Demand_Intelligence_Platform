from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.product import Product
from app.models.store import Store

from app.schemas.sale import SaleCreate
from app.kafka.producer import publish_sale_created_event




def create_sale(db: Session, sale: SaleCreate):

    product = db.query(Product).filter(
        Product.id == sale.product_id
    ).first()

    if not product:
        return None, "Product not found"

    store = db.query(Store).filter(
        Store.id == sale.store_id
    ).first()

    if not store:
        return None, "Store not found"

    db_sale = Sale(
        product_id=sale.product_id,
        store_id=sale.store_id,
        quantity=sale.quantity
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    # Publish event to Kafka
    publish_sale_created_event(db_sale)

    return db_sale, None


def get_all_sales(db: Session):
    return db.query(Sale).all()


def get_sale_by_id(db: Session, sale_id: int):
    return db.query(Sale).filter(
        Sale.id == sale_id
    ).first()


def delete_sale(db: Session, sale_id: int):

    sale = get_sale_by_id(db, sale_id)

    if not sale:
        return None

    db.delete(sale)
    db.commit()

    return sale