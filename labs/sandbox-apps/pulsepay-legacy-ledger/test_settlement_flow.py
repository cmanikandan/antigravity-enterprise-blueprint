#!/usr/bin/env python3
"""Baseline unit test suite for PulsePay Legacy Ledger & Notification Service.

Compatible with both standard-library `python3 -m unittest` and `pytest`.
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

SANDBOX_DIR = Path(__file__).resolve().parent
if str(SANDBOX_DIR) not in sys.path:
    sys.path.insert(0, str(SANDBOX_DIR))

from ledger_batch import (  # noqa: E402
    RECORD_WIDTH,
    calculate_platform_fee_cents,
    load_settlement_batch,
    parse_settlement_line,
    summarize_batch,
)
from notification_service import build_webhook_payload, format_receipt  # noqa: E402


class TestPulsePaySettlementFlow(unittest.TestCase):
    """Baseline tests inherited from the 2021 PulsePay Batch Team."""

    def setUp(self) -> None:
        self.data_path = SANDBOX_DIR / "sample_settlements.dat"
        self.events = load_settlement_batch(self.data_path)

    def test_all_fixed_width_records_are_80_columns(self) -> None:
        raw_lines = [
            line.rstrip("\r\n")
            for line in self.data_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(raw_lines), 8)
        for idx, line in enumerate(raw_lines, start=1):
            self.assertEqual(
                len(line),
                RECORD_WIDTH,
                f"Line {idx} violated 80-byte COBOL copybook width: got {len(line)}",
            )

    def test_parse_settled_record_fields(self) -> None:
        first = self.events[0]
        self.assertEqual(first.record_id, "STL20261115A")
        self.assertEqual(first.merchant_id, "MCH_ACME_001")
        self.assertEqual(first.amount_cents, 125050)
        self.assertEqual(first.currency, "USD")
        self.assertEqual(first.status, "SETTLED")
        self.assertEqual(first.refund_cents, 0)
        self.assertEqual(first.value_date, "20261115")
        self.assertEqual(first.channel, "ACH_CORE_V1")

    def test_batch_summary_counts_and_gross_totals(self) -> None:
        summary = summarize_batch(self.events)
        self.assertEqual(summary["record_count"], 8)
        self.assertEqual(summary["status_counts"]["SETTLED"], 4)
        self.assertEqual(summary["status_counts"]["PART_REFND"], 2)
        self.assertEqual(summary["status_counts"]["HELD"], 1)
        self.assertEqual(summary["status_counts"]["CHARGEBACK"], 1)
        self.assertEqual(summary["gross_cents_by_currency"]["USD"], 1811650)
        self.assertEqual(summary["net_cents_by_currency"]["USD"], 1755125)

    def test_platform_fee_skips_held_and_chargeback(self) -> None:
        settled_event = self.events[1]  # 480000 cents -> 25 bps = 1200 cents
        held_event = self.events[4]
        chargeback_event = self.events[6]
        self.assertEqual(calculate_platform_fee_cents(settled_event), 1200)
        self.assertEqual(calculate_platform_fee_cents(held_event), 0)
        self.assertEqual(calculate_platform_fee_cents(chargeback_event), 0)

    def test_format_receipt_for_standard_settled_and_held_records(self) -> None:
        settled_receipt = format_receipt(self.events[0])
        self.assertIn("Merchant MCH_ACME_001", settled_receipt)
        self.assertIn("Net Payout: USD 1250.50", settled_receipt)

        held_receipt = format_receipt(self.events[4])
        self.assertIn("[HOLD NOTICE]", held_receipt)
        self.assertIn("Held Amount: GBP 7500.00", held_receipt)

    def test_webhook_payload_for_standard_settled_record(self) -> None:
        payload = build_webhook_payload(self.events[1])
        self.assertEqual(payload["record_id"], "STL20261115B")
        self.assertEqual(payload["payout_amount"], "4800.00")

    def test_rejects_malformed_record_width(self) -> None:
        with self.assertRaises(ValueError):
            parse_settlement_line("TOO_SHORT_RECORD")


if __name__ == "__main__":
    unittest.main()
