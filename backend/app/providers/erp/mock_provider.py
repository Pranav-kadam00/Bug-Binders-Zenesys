"""
AQURA ERP Integration — Mock Provider
======================================
Returns realistic responses without hitting any real ERP API.
Used when ERP_PROVIDER=mock (default for development).
"""
from __future__ import annotations

import asyncio
from typing import Any

from .base import ERPConnectionResult, ERPProvider, ERPSyncResult


class MockERPProvider(ERPProvider):
    """
    Fully functional mock that simulates all ERP operations.
    Safe to use in development / demo without any credentials.
    """

    @property
    def name(self) -> str:
        return "Mock ERP"

    async def test_connection(self) -> ERPConnectionResult:
        await asyncio.sleep(0.05)   # simulate network
        return ERPConnectionResult(
            success=True,
            message="Mock ERP connection successful. No real credentials required.",
            provider=self.name,
            account_id="MOCK-ACCOUNT-001",
            environment="sandbox",
            latency_ms=52.0,
        )

    async def sync_vendors(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="vendors",
            records_processed=5, records_created=0, records_updated=5,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def sync_items(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="items",
            records_processed=12, records_created=2, records_updated=10,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def sync_purchase_orders(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="purchase_orders",
            records_processed=3, records_created=1, records_updated=2,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def sync_inventory(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="inventory",
            records_processed=8, records_created=0, records_updated=8,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def sync_departments(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="departments",
            records_processed=6, records_created=0, records_updated=6,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def sync_employees(self) -> ERPSyncResult:
        return ERPSyncResult(
            success=True, entity="employees",
            records_processed=4, records_created=0, records_updated=4,
            started_at=self._now(), completed_at=self._now(), provider=self.name,
        )

    async def get_sync_status(self) -> dict[str, Any]:
        return {
            "provider": self.name,
            "environment": "sandbox",
            "last_sync": self._now(),
            "entities": {
                "vendors":        {"status": "synced", "count": 5},
                "items":          {"status": "synced", "count": 12},
                "purchase_orders":{"status": "synced", "count": 3},
                "inventory":      {"status": "synced", "count": 8},
                "departments":    {"status": "synced", "count": 6},
                "employees":      {"status": "synced", "count": 4},
            },
        }
