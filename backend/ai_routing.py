import random

def get_optimal_route(transaction_data: dict) -> str:
    """
    Basic AI routing logic: for failed transactions, choose an alternative route.
    Otherwise, return the primary route.
    """
    if transaction_data.get("status") == "failed":
        return random.choice(["Route B", "Route C"])
    else:
        return "Route A"
