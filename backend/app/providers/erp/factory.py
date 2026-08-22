"""
ERP Provider Factory
====================
Reads ERP_PROVIDER from environment and returns the appropriate provider.

Supported values:
  mock       — MockERPProvider  (default, no credentials needed)
  netsuite   — NetSuiteProvider
  (future: sap, oracle, dynamics)

Usage:
  from app.providers.erp import get_erp_provider
  erp = get_erp_provider()
  result = await erp.test_connection()
"""
from __future__ import annotations

import os

from .base import ERPProvider
from .mock_provider import MockERPProvider
from .netsuite_provider import NetSuiteProvider

_REGISTRY: dict[str, type[ERPProvider]] = {
    "mock":     MockERPProvider,
    "netsuite": NetSuiteProvider,
}


def get_erp_provider(provider_name: str | None = None) -> ERPProvider:
    """
    Return an initialized ERP provider instance.

    Args:
        provider_name: Override the ERP_PROVIDER env var (useful in tests).

    Returns:
        An ERPProvider instance.
    """
    name = (provider_name or os.getenv("ERP_PROVIDER", "mock")).lower().strip()
    cls = _REGISTRY.get(name)
    if cls is None:
        available = ", ".join(_REGISTRY.keys())
        raise ValueError(
            f"Unknown ERP provider '{name}'. "
            f"Available providers: {available}. "
            f"Set ERP_PROVIDER in your .env file."
        )
    return cls()
