
import asyncio
import pytest

from app.services.order_service import get_order
from app.services.escalation_service import (
    create_escalation,
    get_escalations,
    ESCALATION_QUEUE
)


# ORDER SERVICE TESTS

def test_valid_order():
    result = asyncio.run(get_order("ORD1001"))

    assert result["status"] == "Shipped"
    assert result["delivery_days"] == 2


def test_order_id_case_insensitive():
    result = asyncio.run(get_order("ord1001"))

    assert result is not None


def test_unknown_order():
    result = asyncio.run(get_order("ORD9999"))

    assert result is None


def test_order_service_error():
    with pytest.raises(RuntimeError):
        asyncio.run(get_order("ORD1001", "error"))


def test_malformed_order_response():
    result = asyncio.run(get_order("ORD1001", "malformed"))

    assert "status" not in result


# ESCALATION SERVICE TESTS

def test_create_escalation():
    ESCALATION_QUEUE.clear()

    ticket = create_escalation(
        "Where is my order?",
        "Order information unavailable"
    )

    assert ticket["question"] == "Where is my order?"
    assert ticket["status"] == "open"
    assert ticket["ticket_id"]


def test_escalation_queue():
    ESCALATION_QUEUE.clear()

    create_escalation("Test question")

    tickets = get_escalations()

    assert len(tickets) == 1
    assert tickets[0]["status"] == "open"


def test_unique_ticket_ids():
    ESCALATION_QUEUE.clear()

    first = create_escalation("Question one")
    second = create_escalation("Question two")

    assert first["ticket_id"] != second["ticket_id"]
