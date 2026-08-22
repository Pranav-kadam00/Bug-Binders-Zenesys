from __future__ import annotations

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Canonical product aliases — maps common variant names to a normalised key.
# Matching is case-insensitive and ignores punctuation.
# ---------------------------------------------------------------------------
_PRODUCT_ALIASES: dict[str, list[str]] = {
    "business laptop": ["laptop", "laptops", "notebook", "notebooks", "workstation"],
    "ergonomic office chair": ["chair", "chairs", "office chair", "seating"],
    "cement": ["cement bag", "cement bags", "opc cement", "ppc cement"],
    "cloud observability license": ["observability", "monitoring license", "datadog", "apm license"],
    "industrial equipment": ["industrial", "machinery", "equipment"],
    "packaging boxes": ["boxes", "box", "carton", "cartons", "packaging"],
}

# Reverse lookup: alias → canonical
_ALIAS_LOOKUP: dict[str, str] = {}
for _canonical, _aliases in _PRODUCT_ALIASES.items():
    for _alias in _aliases:
        _ALIAS_LOOKUP[_alias] = _canonical


def _normalise(text: str) -> str:
    """Lowercase, strip leading/trailing whitespace, collapse inner whitespace."""
    return re.sub(r"\s+", " ", text.strip().lower())


def _canonical_product(name: str) -> str:
    """Return the canonical product name, following alias table if needed."""
    n = _normalise(name)
    if n in _ALIAS_LOOKUP:
        return _ALIAS_LOOKUP[n]
    return n


def _products_match(requested: str, available: str) -> bool:
    """
    True when requested product matches an available capability.

    Priority:
    1. Exact normalised match.
    2. Canonical alias match (both sides resolved).
    3. Substring containment (either direction).
    """
    req_n = _normalise(requested)
    avail_n = _normalise(available)

    if req_n == avail_n:
        return True

    # Resolve through alias table
    req_c = _canonical_product(req_n)
    avail_c = _canonical_product(avail_n)
    if req_c == avail_c:
        return True

    # Substring containment (fuzzy fallback)
    if req_n in avail_n or avail_n in req_n:
        return True

    # Canonical substring
    if req_c in avail_c or avail_c in req_c:
        return True

    return False


_ACTIVE_STATUSES = {"active", "preferred", "verified"}


class VendorCapacityService:
    """
    Decides whether a vendor can fulfil a given product request.

    KEY FIX (2026-08-22):
    ─────────────────────
    Previously the ``deliveryRadiusKm`` field (a vendor's *local last-mile*
    radius) was compared against the *buyer-to-vendor haversine distance*.
    These are unrelated concepts:

    • deliveryRadiusKm  — how far the vendor's own trucks go for free/standard
      delivery (a vendor in Mumbai might deliver within 50 km of Mumbai).
    • distance_km       — how far the vendor is from the buyer (Mumbai to Pune
      is ~120 km).

    Filtering on ``dist > deliveryRadiusKm`` incorrectly excluded every vendor
    more than a few dozen kilometres away, producing zero results.

    The discovery *search radius* is enforced by ``VendorDiscoveryService``
    before calling this method.  This service only evaluates stock / quantity /
    status / product fit.  Delivery availability is used for *scoring* only.
    """

    def qualify(
        self,
        vendor: dict,
        product_name: str,
        category: Optional[str],
        quantity: float,
        distance_km: float,
        allow_partial: bool = False,
    ) -> Optional[dict]:
        # ── 1. Vendor status ─────────────────────────────────────────────────
        status = vendor.get("status", "").strip().lower()
        if status not in _ACTIVE_STATUSES:
            return None

        # ── 2. Bulk order support ────────────────────────────────────────────
        if not vendor.get("bulkOrderSupported", False):
            return None

        # ── 3. Find matching capability ──────────────────────────────────────
        capabilities: list[dict] = vendor.get("capabilities", [])
        capability: Optional[dict] = None

        # Exact / fuzzy product name match
        for cap in capabilities:
            if _products_match(product_name, cap.get("productName", "")):
                capability = cap
                break

        # Category-level fallback: use defaultCapability when category matches
        if capability is None and category:
            vendor_category = _normalise(vendor.get("category", ""))
            req_category = _normalise(category)
            if vendor_category == req_category or req_category in vendor_category:
                capability = vendor.get("defaultCapability")

        if capability is None:
            return None

        # ── 4. Quantity checks ───────────────────────────────────────────────
        available: float = float(capability.get("availableQuantity", 0))
        max_capacity: float = float(
            capability.get("maximumOrderCapacity", available) or available
        )
        min_order: float = float(
            capability.get("minimumOrderQuantity",
                           vendor.get("minimumOrderQuantity", 0)) or 0
        )

        if not allow_partial:
            if available < quantity or max_capacity < quantity:
                return None

        if quantity < min_order and min_order > 0:
            return None

        # ── 5. NOTE: delivery radius is NOT a hard exclusion ─────────────────
        # It is used as a scoring signal in VendorRankingService.
        # Removing it here was the primary bug fix.

        fulfil_qty = min(available, quantity) if allow_partial else quantity

        return {
            "capability": capability,
            "available_quantity": available,
            "fulfillment_quantity": fulfil_qty,
            "distance_km": distance_km,
            # Expose delivery availability for ranking
            "delivery_available": capability.get("deliveryAvailable", True),
            "within_delivery_radius": distance_km <= vendor.get("deliveryRadiusKm", 9999),
        }
