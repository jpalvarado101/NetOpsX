import random

def get_optimal_route(transaction_data: dict) -> str:
    """
    Implements basic AI routing logic:
    - Returns "Route A" if the transaction is successful.
    - Returns an alternative route (either "Route B" or "Route C") if failed.
    """
    if transaction_data.get("status") == "failed":
        return random.choice(["Route B", "Route C"])
    else:
        return "Route A"
