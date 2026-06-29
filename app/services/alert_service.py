def detect_demand_spike(quantity: int):

    SPIKE_THRESHOLD = 50

    if quantity >= SPIKE_THRESHOLD:

        print(
            f"🚨 DEMAND SPIKE DETECTED! "
            f"Quantity sold: {quantity}"
        )
        