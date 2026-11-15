#!/usr/bin/env python3
"""PulsePay Legacy Nightly Settlement Batch Processor (v1.4 - Legacy Core).

Parses 80-column fixed-width COBOL-style settlement records from
`sample_settlements.dat` and emits `SettlementEvent` objects for downstream
treasury reconciliation and merchant receipt notifications.

Fixed-Width 80-Character Copybook Layout (`PPAY-STL-80`):
  Cols 00..12 (12) : RECORD_ID     (e.g. 'STL20261115A')
  Cols 12..24 (12) : MERCHANT_ID   (e.g. 'MCH_ACME_001')
  Cols 24..36 (12) : AMOUNT_CENTS  (zero-padded integer minor units)
  Cols 36..39 (03) : CURRENCY      (ISO-4217 code: USD, EUR, GBP)
  Cols 39..49 (10) : STATUS        (SETTLED, PART_REFND, HELD, CHARGEBACK)
  Cols 49..61 (12) : REFUND_CENTS  (zero-padded integer minor units)
  Cols 61..69 (08) : VALUE_DATE    (YYYYMMDD)
  Cols 69..80 (11) : CHANNEL       (settlement rail identifier)
"""

from __future__ import annotations

from dataclasses import dataclass
import datetime
import json
from pathlib import Path
from typing import Any

RECORD_WIDTH = 80

# Legacy hardcoded operational constants (scheduled for 12-Factor / Cloud Run refactor)
HARDCODED_SPOOL_DIR = "/var/spool/pulsepay/ach_outbox"
LEGACY_TREASURY_DSN = "postgres://pulsepay_batch:local_placeholder_only@10.240.12.9:5432/ledger"
LEGACY_BATCH_HMAC_SEED = "SYNTHETIC_DEV_SEED_DO_NOT_USE_IN_PROD"
PLATFORM_FEE_BPS = 25  # 25 basis points (0.25%)


@dataclass(frozen=True)
class SettlementEvent:
    """Domain event emitted by the PulsePay fixed-width batch parser."""

    record_id: str
    merchant_id: str
    amount_cents: int
    currency: str
    status: str
    refund_cents: int
    value_date: str
    channel: str
    ingested_at_iso: str

    @property
    def net_amount_cents(self) -> int:
        """Returns gross settlement minus any partial refund or chargeback in integer cents."""
        return self.amount_cents - self.refund_cents

    @property
    def net_settlement_dollars(self) -> float:
        """Legacy helper added in 2021 for CSV exports — returns major currency units (dollars)."""
        return (self.amount_cents - self.refund_cents) / 100.0


def parse_settlement_line(raw_line: str) -> SettlementEvent:
    """Parses a single 80-character fixed-width settlement record."""
    line = raw_line.rstrip("\r\n")
    if len(line) != RECORD_WIDTH:
        raise ValueError(
            f"Invalid fixed-width record length: expected {RECORD_WIDTH} chars, got {len(line)}"
        )

    record_id = line[0:12].strip()
    merchant_id = line[12:24].strip()
    amount_cents = int(line[24:36])
    currency = line[36:39].strip()
    status = line[39:49].strip()
    refund_cents = int(line[49:61])
    value_date = line[61:69].strip()
    channel = line[69:80].strip()

    # Legacy Python <3.12 naive UTC timestamp anti-pattern
    ingested_at = datetime.datetime.utcnow().isoformat() + "Z"

    return SettlementEvent(
        record_id=record_id,
        merchant_id=merchant_id,
        amount_cents=amount_cents,
        currency=currency,
        status=status,
        refund_cents=refund_cents,
        value_date=value_date,
        channel=channel,
        ingested_at_iso=ingested_at,
    )


def load_settlement_batch(data_file: str | Path | None = None) -> list[SettlementEvent]:
    """Loads all settlement records from the fixed-width `.dat` batch file."""
    target = (
        Path(data_file)
        if data_file is not None
        else Path(__file__).resolve().parent / "sample_settlements.dat"
    )
    events: list[SettlementEvent] = []
    with target.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if not raw_line.strip():
                continue
            events.append(parse_settlement_line(raw_line))
    return events


def calculate_platform_fee_cents(event: SettlementEvent) -> int:
    """Computes platform treasury fee in integer cents for settled or partially refunded payouts."""
    if event.status in ("HELD", "CHARGEBACK"):
        return 0
    return (event.net_amount_cents * PLATFORM_FEE_BPS) // 10_000


def summarize_batch(events: list[SettlementEvent]) -> dict[str, Any]:
    """Produces an aggregate reconciliation summary across all currencies and statuses."""
    by_status: dict[str, int] = {}
    gross_cents_by_currency: dict[str, int] = {}
    net_cents_by_currency: dict[str, int] = {}
    total_fee_cents = 0

    for ev in events:
        by_status[ev.status] = by_status.get(ev.status, 0) + 1
        gross_cents_by_currency[ev.currency] = (
            gross_cents_by_currency.get(ev.currency, 0) + ev.amount_cents
        )
        net_cents_by_currency[ev.currency] = (
            net_cents_by_currency.get(ev.currency, 0) + ev.net_amount_cents
        )
        total_fee_cents += calculate_platform_fee_cents(ev)

    # Legacy Python <3.12 naive UTC timestamp anti-pattern
    generated_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "record_count": len(events),
        "status_counts": by_status,
        "gross_cents_by_currency": gross_cents_by_currency,
        "net_cents_by_currency": net_cents_by_currency,
        "platform_fee_cents": total_fee_cents,
        "spool_target": HARDCODED_SPOOL_DIR,
        "generated_at": generated_at,
    }


def main() -> int:
    events = load_settlement_batch()
    summary = summarize_batch(events)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
