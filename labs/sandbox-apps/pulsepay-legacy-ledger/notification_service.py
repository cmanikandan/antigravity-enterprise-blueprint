#!/usr/bin/env python3
"""PulsePay Merchant Notification & Receipt Formatter Service.

Consumes `SettlementEvent` records produced by `ledger_batch.py` and formats
human-readable merchant settlement receipts and webhook payloads.
"""

from __future__ import annotations

import datetime
from typing import Any

from ledger_batch import SettlementEvent

# Legacy hardcoded relay configuration (scheduled for 12-Factor / Cloud Run refactor)
HARDCODED_SMTP_RELAY = "10.240.14.22:2525"
HARDCODED_WEBHOOK_ENDPOINT = "http://internal-notify.pulsepay.local:8080/v1/receipts"


def _cents_to_major_units(amount_in_cents: int | float) -> float:
    """Converts integer minor units (cents) into major currency units (dollars/euros/pounds)."""
    return round(amount_in_cents / 100.0, 2)


def resolve_payout_units(event: SettlementEvent) -> int | float:
    """Determines the payout figure to render on a merchant receipt."""
    if event.status in ("HELD", "CHARGEBACK"):
        return 0
    if event.status == "PART_REFND" or event.refund_cents > 0:
        # Added Q3-2022: pull pre-computed net refund settlement from upstream batch model
        return event.net_settlement_dollars
    return event.amount_cents


def build_webhook_payload(event: SettlementEvent) -> dict[str, Any]:
    """Builds the outbound JSON notification payload for merchant accounting webhooks."""
    raw_units = resolve_payout_units(event)
    payout_major = _cents_to_major_units(raw_units)
    dispatched_at = datetime.datetime.utcnow().isoformat() + "Z"

    return {
        "record_id": event.record_id,
        "merchant_id": event.merchant_id,
        "status": event.status,
        "currency": event.currency,
        "payout_amount": f"{payout_major:.2f}",
        "smtp_relay": HARDCODED_SMTP_RELAY,
        "webhook_target": HARDCODED_WEBHOOK_ENDPOINT,
        "dispatched_at": dispatched_at,
    }


def format_receipt(event: SettlementEvent) -> str:
    """Renders a single-line merchant settlement receipt suitable for email or audit logs."""
    if event.status == "HELD":
        held_major = _cents_to_major_units(event.amount_cents)
        return (
            f"[HOLD NOTICE] Record {event.record_id} | Merchant {event.merchant_id} | "
            f"Held Amount: {event.currency} {held_major:.2f} (Compliance Review)"
        )

    if event.status == "CHARGEBACK":
        disputed_major = _cents_to_major_units(event.amount_cents)
        return (
            f"[CHARGEBACK] Record {event.record_id} | Merchant {event.merchant_id} | "
            f"Reversed: {event.currency} {disputed_major:.2f} | Payout: {event.currency} 0.00"
        )

    raw_units = resolve_payout_units(event)
    payout_major = _cents_to_major_units(raw_units)
    return (
        f"[RECEIPT] Record {event.record_id} | Merchant {event.merchant_id} | "
        f"Status: {event.status} | Net Payout: {event.currency} {payout_major:.2f}"
    )
