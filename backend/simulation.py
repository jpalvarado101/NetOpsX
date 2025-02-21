import random

def simulate_transaction() -> dict:
    """
    Simulates a transaction event.
    Randomly returns a transaction status of either 'successful' or 'failed'.
    """
    status = random.choice(["successful", "failed"])
    return {"status": status}
