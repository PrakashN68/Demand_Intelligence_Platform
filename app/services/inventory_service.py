from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate


def create_inventory(
        db: Session,
        inventory: InventoryCreate
):

    db_inventory = Inventory(
        product_id=inventory.product_id,
        store_id=inventory.store_id,
        stock_on_hand=inventory.stock_on_hand,
        reorder_point=inventory.reorder_point
    )

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def get_all_inventory(db: Session):
    return db.query(Inventory).all()

def reduce_inventory(
        db: Session,
        product_id: int,
        store_id: int,
        quantity: int
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id,
            Inventory.store_id == store_id
        )
        .first()
    )

    if not inventory:
        print(
            f"No inventory found for "
            f"Product {product_id}, Store {store_id}"
        )
        return

    inventory.stock_on_hand -= quantity

    db.commit()

    print(
        f"Inventory updated. "
        f"Remaining stock: {inventory.stock_on_hand}"
    )

    # Low inventory check
    if inventory.stock_on_hand <= inventory.reorder_point:

        print(
            f"🚨 LOW INVENTORY ALERT | "
            f"Product: {product_id} | "
            f"Store: {store_id} | "
            f"Current Stock: {inventory.stock_on_hand} | "
            f"Reorder Point: {inventory.reorder_point}"
        )