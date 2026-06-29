import json

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",

    value_serializer=lambda v:
        json.dumps(v).encode("utf-8")
)


def publish_sale_created_event(sale):

    event = {
        "sale_id": sale.id,
        "product_id": sale.product_id,
        "store_id": sale.store_id,
        "quantity": sale.quantity
    }

    producer.send(
        "sale_created",
        value=event
    )

    producer.flush()

    print(f"Published event: {event}")
    