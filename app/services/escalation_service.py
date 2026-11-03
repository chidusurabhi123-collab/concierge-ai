
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

STORAGE_FILE = Path("storage/escalations.json")

STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_escalations() -> list[dict]:
    if not STORAGE_FILE.exists():
        return []

    with STORAGE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


ESCALATION_QUEUE = load_escalations()


def save_escalations():
    temporary_file = STORAGE_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(ESCALATION_QUEUE, file, indent=2)

    temporary_file.replace(STORAGE_FILE)


def create_escalation(
    question: str,
    reason: str = "Insufficient information"
) -> dict:

    ticket = {
        "ticket_id": str(uuid4()),
        "question": question,
        "reason": reason,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    ESCALATION_QUEUE.append(ticket)
    save_escalations()

    return ticket


def get_escalations() -> list[dict]:
    return ESCALATION_QUEUE
