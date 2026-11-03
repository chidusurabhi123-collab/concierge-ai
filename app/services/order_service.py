import asyncio

ORDERS = {
    "ORD1001": {"status": "Shipped", "delivery_days": 2},
    "ORD1002": {"status": "Processing", "delivery_days": 5},
    "ORD1003": {"status": "Delivered", "delivery_days": 0}
}


async def get_order(order_id: str, simulate: str = "none"):
    if simulate == "slow":
        await asyncio.sleep(5)

    if simulate == "error":
        raise RuntimeError("Mock order service unavailable")

    if simulate == "malformed":
        return {"unexpected_field": None}

    return ORDERS.get(order_id.upper())


async def get_order_async(order_id: str, simulate: str = "none"):
    return await get_order(order_id, simulate)