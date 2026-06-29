import json
from app.db.database import SessionLocal
from app.services.daily_demand_service import update_daily_demand_summary
from kafka import KafkaConsumer
from app.services.alert_service import detect_demand_spike
from app.services.inventory_service import reduce_inventory



consumer = KafkaConsumer(
    "sale_created",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="earliest",

    value_deserializer=lambda m:
        json.loads(m.decode("utf-8"))
)


print("Listening for sale events...")

for message in consumer:

    event = message.value

    print(f"Received Sale Event: {event}")

    quantity = event.get("quantity")

    # Validate quantity
    if quantity is None:
        print("Quantity missing. Skipping event.")
        continue

    if quantity <= 0:
        print("Invalid quantity. Skipping event.")
        continue

    db = SessionLocal()

    try:
        update_daily_demand_summary(
            db=db,
            quantity=quantity
        )

        reduce_inventory(
        db=db,
        product_id=event["product_id"],
        store_id=event["store_id"],
        quantity=quantity
    )

        detect_demand_spike(quantity)

        print("Daily demand summary updated")

    finally:
        db.close()

    

    