"""
AQURA ERP Integration — NetSuite Provider
==========================================
Implements the ERPProvider interface for Oracle NetSuite.

Authentication modes supported (set via NETSUITE_AUTH_MODE):
  • token_based   — TBA (Token-Based Authentication) via Consumer/Token keys
  • oauth2        — OAuth 2.0 Client Credentials
  • mock          — No real API calls (safe for demo / CI)

Configuration is entirely environment-variable driven.
No source code changes are needed to switch between sandbox and production.

Required env vars (token_based):
  NETSUITE_ACCOUNT_ID
  NETSUITE_CONSUMER_KEY, NETSUITE_CONSUMER_SECRET
  NETSUITE_TOKEN_ID,     NETSUITE_TOKEN_SECRET

Required env vars (oauth2):
  NETSUITE_ACCOUNT_ID
  NETSUITE_CLIENT_ID, NETSUITE_CLIENT_SECRET

Optional:
  NETSUITE_BASE_URL          (auto-derived from ACCOUNT_ID if omitted)
  NETSUITE_INTEGRATION_MODE  mock | sandbox | production  (default: mock)
  NETSUITE_MAX_RETRIES       (default: 3)
"""
from __future__ import annotations

import os
from typing import Any

from .base import ERPConnectionResult, ERPProvider, ERPSyncResult


class NetSuiteProvider(ERPProvider):
    """
    NetSuite ERP provider.

    When NETSUITE_INTEGRATION_MODE=mock (default) all operations return
    realistic stub data without making real HTTP calls — ideal for development
    and demos without a NetSuite account.
    """

    # ── Configuration ─────────────────────────────────────────────────────────

    def __init__(self) -> None:
        self.account_id  = os.getenv("NETSUITE_ACCOUNT_ID", "")
        self.auth_mode   = os.getenv("NETSUITE_AUTH_MODE", "mock")
        self.mode        = os.getenv("NETSUITE_INTEGRATION_MODE", "mock")
        self.max_retries = int(os.getenv("NETSUITE_MAX_RETRIES", "3"))
        self.sync_enabled = os.getenv("NETSUITE_SYNC_ENABLED", "false").lower() == "true"

        # TBA credentials
        self.consumer_key    = os.getenv("NETSUITE_CONSUMER_KEY", "")
        self.consumer_secret = os.getenv("NETSUITE_CONSUMER_SECRET", "")
        self.token_id        = os.getenv("NETSUITE_TOKEN_ID", "")
        self.token_secret    = os.getenv("NETSUITE_TOKEN_SECRET", "")

        # OAuth2 credentials
        self.client_id     = os.getenv("NETSUITE_CLIENT_ID", "")
        self.client_secret = os.getenv("NETSUITE_CLIENT_SECRET", "")

        # Derive base URL from account ID if not explicitly set
        raw_base = os.getenv("NETSUITE_BASE_URL", "")
        if raw_base:
            self.base_url = raw_base.rstrip("/")
        elif self.account_id:
            acct = self.account_id.lower().replace("_", "-")
            self.base_url = f"https://{acct}.suitetalk.api.netsuite.com/services/rest/record/v1"
        else:
            self.base_url = ""

        # Currency mapping — maps Aqura default currency to NetSuite internal ID
        # Configurable per account since internal IDs differ between accounts.
        self.currency_map: dict[str, str] = {
            "INR": os.getenv("NETSUITE_CURRENCY_INR_ID", "1"),
            "USD": os.getenv("NETSUITE_CURRENCY_USD_ID", "2"),
        }

    # ── Interface ─────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "NetSuite"

    async def test_connection(self) -> ERPConnectionResult:
        if self.mode == "mock" or not self.account_id:
            return ERPConnectionResult(
                success=True,
                message=(
                    "NetSuite provider is in mock mode. "
                    "Set NETSUITE_ACCOUNT_ID and NETSUITE_INTEGRATION_MODE=sandbox|production "
                    "to connect to a real NetSuite account."
                ),
                provider=self.name,
                account_id=self.account_id or "NOT_CONFIGURED",
                environment=self.mode,
                latency_ms=12.0,
            )
        # Real connection test
        try:
            latency = await self._ping()
            return ERPConnectionResult(
                success=True,
                message=f"NetSuite connection verified ({self.mode}).",
                provider=self.name,
                account_id=self.account_id,
                environment=self.mode,
                latency_ms=latency,
            )
        except Exception as exc:
            return ERPConnectionResult(
                success=False,
                message=f"NetSuite connection failed: {exc}",
                provider=self.name,
                account_id=self.account_id,
                environment=self.mode,
            )

    async def sync_vendors(self) -> ERPSyncResult:
        return await self._sync("vendors", "vendor")

    async def sync_items(self) -> ERPSyncResult:
        return await self._sync("items", "inventoryItem")

    async def sync_purchase_orders(self) -> ERPSyncResult:
        return await self._sync("purchase_orders", "purchaseOrder")

    async def sync_inventory(self) -> ERPSyncResult:
        return await self._sync("inventory", "inventoryItem")

    async def sync_departments(self) -> ERPSyncResult:
        return await self._sync("departments", "department")

    async def sync_employees(self) -> ERPSyncResult:
        return await self._sync("employees", "employee")

    async def get_sync_status(self) -> dict[str, Any]:
        return {
            "provider": self.name,
            "environment": self.mode,
            "account_id": self.account_id or "NOT_CONFIGURED",
            "auth_mode": self.auth_mode,
            "sync_enabled": self.sync_enabled,
            "base_url": self.base_url or "NOT_CONFIGURED",
            "currency_map": self.currency_map,
            "entities": {
                "vendors":         {"status": "pending"},
                "items":           {"status": "pending"},
                "purchase_orders": {"status": "pending"},
                "inventory":       {"status": "pending"},
                "departments":     {"status": "pending"},
                "employees":       {"status": "pending"},
            },
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    async def _sync(self, entity: str, netsuite_record_type: str) -> ERPSyncResult:
        """Unified sync entry point — real or mock depending on mode."""
        if self.mode == "mock" or not self.account_id:
            return ERPSyncResult(
                success=True, entity=entity,
                records_processed=0, records_created=0, records_updated=0,
                errors=[], started_at=self._now(), completed_at=self._now(),
                provider=self.name,
            )
        # Real implementation — fetches from NetSuite REST API
        try:
            records = await self._fetch_records(netsuite_record_type)
            return ERPSyncResult(
                success=True, entity=entity,
                records_processed=len(records),
                records_updated=len(records),
                started_at=self._now(), completed_at=self._now(),
                provider=self.name,
            )
        except Exception as exc:
            return ERPSyncResult(
                success=False, entity=entity,
                errors=[str(exc)],
                started_at=self._now(), completed_at=self._now(),
                provider=self.name,
            )

    async def _ping(self) -> float:
        """Quick connectivity check — returns latency in ms."""
        import time, urllib.request
        url = f"{self.base_url}/vendor?limit=1"
        headers = self._auth_headers()
        req = urllib.request.Request(url, headers=headers)
        t0 = time.monotonic()
        with urllib.request.urlopen(req, timeout=10):
            pass
        return round((time.monotonic() - t0) * 1000, 1)

    async def _fetch_records(self, record_type: str, limit: int = 1000) -> list[dict]:
        """Fetch records from NetSuite REST Record API."""
        import json, urllib.request
        url = f"{self.base_url}/{record_type}?limit={limit}"
        headers = self._auth_headers()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        return data.get("items", [])

    def _auth_headers(self) -> dict[str, str]:
        """Build HTTP Authorization header based on auth_mode."""
        if self.auth_mode == "token_based":
            return {"Authorization": self._tba_header(), "Content-Type": "application/json"}
        elif self.auth_mode == "oauth2":
            return {"Authorization": f"Bearer {self._get_oauth2_token()}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}

    def _tba_header(self) -> str:
        """Generate OAuth 1.0a TBA Authorization header."""
        import base64, hashlib, hmac, time, uuid
        timestamp = str(int(time.time()))
        nonce = uuid.uuid4().hex
        base = "&".join([
            "GET",
            urllib_quote(f"{self.base_url}/"),
            urllib_quote("&".join([
                f"oauth_consumer_key={self.consumer_key}",
                f"oauth_nonce={nonce}",
                "oauth_signature_method=HMAC-SHA256",
                f"oauth_timestamp={timestamp}",
                f"oauth_token={self.token_id}",
                "oauth_version=1.0",
            ])),
        ])
        key = f"{self.consumer_secret}&{self.token_secret}"
        sig = base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha256).digest()).decode()
        return (
            f'OAuth realm="{self.account_id}",'
            f'oauth_consumer_key="{self.consumer_key}",'
            f'oauth_token="{self.token_id}",'
            f'oauth_signature_method="HMAC-SHA256",'
            f'oauth_timestamp="{timestamp}",'
            f'oauth_nonce="{nonce}",'
            f'oauth_version="1.0",'
            f'oauth_signature="{sig}"'
        )

    def _get_oauth2_token(self) -> str:
        """Obtain OAuth2 client_credentials token."""
        import json, urllib.parse, urllib.request
        data = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }).encode()
        acct = self.account_id.lower().replace("_", "-")
        url = f"https://{acct}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())["access_token"]


def urllib_quote(s: str) -> str:
    from urllib.parse import quote
    return quote(s, safe="")
