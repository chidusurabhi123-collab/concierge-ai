from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.services.order_service import get_order

router = APIRouter()


@router.get("/orders/{order_id}")
async def lookup_order(
    order_id: str,
    simulate: Literal["none", "slow", "error", "malformed"] = Query(
        default="none"
    )
):
    try:
        order = await get_order(order_id, simulate)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        if not isinstance(order, dict) or not {
            "status", "delivery_days"
        }.issubset(order):
            raise HTTPException(
                status_code=502,
                detail="Invalid response from order service"
            )

        return {
            "order_id": order_id.upper(),
            **order
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Order service temporarily unavailable"
        )