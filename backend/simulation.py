import random

def simulate_transaction() -> dict:
    """
    Simulate a transaction event.
    Randomly returns a transaction status as either 'successful' or 'failed'.
    """
    status = random.choice(["successful", "failed"])
    return {"status": status}
