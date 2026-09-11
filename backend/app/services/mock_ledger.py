"""Provider-neutral mock ledger helpers used for demo-only transactions."""

import asyncio
import random
import time
from typing import Optional

from app.models import TransactionRecord


def _mock_reference() -> str:
    return f"EP-MOCK-{int(time.time() * 1000)}-{random.randint(0, 9999)}"


async def create_transfer(amount: Optional[int], recipient: Optional[str]) -> dict:
    await asyncio.sleep(1.0)
    return {
        "status": "success",
        "reference": _mock_reference(),
        "amount": amount,
        "recipient": recipient,
        "environment": "sandbox-mock",
    }


async def get_transaction_status(reference: str) -> dict:
    await asyncio.sleep(0.25)
    return {"status": "confirmed", "reference": reference, "environment": "sandbox-mock"}


async def get_account_balance(account_id: str) -> dict:
    await asyncio.sleep(0.2)
    return {"accountId": account_id, "balance": 300000, "currency": "NGN", "environment": "sandbox-mock"}


def generate_receipt(tx: TransactionRecord) -> dict:
    """Mark real receipts by their provider reference rather than mock prefix."""
    is_real = bool(tx.paymentReference) and not tx.paymentReference.startswith("EP-MOCK-")
    return {
        "transactionId": tx.id,
        "type": tx.action,
        "amount": tx.amount,
        "recipient": tx.recipient,
        "reference": tx.paymentReference,
        "status": tx.state,
        "date": tx.createdAt,
        "environment": "sandbox-live" if is_real else "sandbox-mock",
    }
