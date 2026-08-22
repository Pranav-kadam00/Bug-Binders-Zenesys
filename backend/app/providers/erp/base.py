"""
AQURA ERP Integration — Base Provider Interface
===============================================
All ERP providers (NetSuite, SAP, Oracle, Mock, etc.) must implement
this interface.  The application selects a provider at runtime via the
ERP_PROVIDER environment variable — no source code changes required.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ERPConnectionResult:
    success: bool
    message: str
    provider: str
    account_id: Optional[str] = None
    environment: str = "mock"
    latency_ms: Optional[float] = None


@dataclass
class ERPSyncResult:
    success: bool
    entity: str                        # "vendors", "items", "purchase_orders", etc.
    records_processed: int = 0
    records_created: int = 0
    records_updated: int = 0
    records_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    provider: str = "mock"

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "entity": self.entity,
            "records_processed": self.records_processed,
            "records_created": self.records_created,
            "records_updated": self.records_updated,
            "records_skipped": self.records_skipped,
            "errors": self.errors,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "provider": self.provider,
        }


class ERPProvider(ABC):
    """
    Abstract base class for all ERP integration providers.

    Extend this class and implement all abstract methods to add a new
    ERP system.  Register the new provider in factory.py.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name, e.g. 'NetSuite', 'SAP', 'Mock'."""

    @abstractmethod
    async def test_connection(self) -> ERPConnectionResult:
        """Verify connectivity and authentication."""

    @abstractmethod
    async def sync_vendors(self) -> ERPSyncResult:
        """Pull vendor / supplier records from the ERP."""

    @abstractmethod
    async def sync_items(self) -> ERPSyncResult:
        """Pull inventory item / product records from the ERP."""

    @abstractmethod
    async def sync_purchase_orders(self) -> ERPSyncResult:
        """Push or pull purchase orders between Aqura and the ERP."""

    @abstractmethod
    async def sync_inventory(self) -> ERPSyncResult:
        """Synchronise inventory levels."""

    @abstractmethod
    async def sync_departments(self) -> ERPSyncResult:
        """Synchronise department / subsidiary records."""

    @abstractmethod
    async def sync_employees(self) -> ERPSyncResult:
        """Synchronise employee / requestor records for mapping."""

    @abstractmethod
    async def get_sync_status(self) -> dict[str, Any]:
        """Return current sync status for all entities."""

    # ── Optional helpers — providers may override ─────────────────────────────

    async def sync_all(self) -> list[ERPSyncResult]:
        """Run all sync operations in sequence."""
        results = []
        for fn in (
            self.sync_vendors,
            self.sync_items,
            self.sync_purchase_orders,
            self.sync_inventory,
            self.sync_departments,
            self.sync_employees,
        ):
            results.append(await fn())
        return results

    def _now(self) -> str:
        return datetime.utcnow().isoformat() + "Z"
