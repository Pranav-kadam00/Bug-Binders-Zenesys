from __future__ import annotations

from typing import Any


class MultiVendorFulfillmentService:
    """Greedy allocation for an optional split order."""

    def allocate(self, matches: list[dict[str, Any]], required_quantity: float) -> dict[str, Any]:
        remaining = required_quantity
        allocations = []
        for match in sorted(matches, key=lambda item: item.get("overall_score", 0), reverse=True):
            capability = match["capability"]
            available = min(match.get("available_quantity", 0), capability.get("maximumOrderCapacity", 0))
            minimum = capability.get("minimumOrderQuantity", 0)
            quantity = min(available, remaining)
            if quantity < minimum:
                continue
            allocations.append({"vendor_id": match["vendor"]["id"], "vendor_name": match["vendor"]["companyName"], "quantity": quantity, "unit_price": match.get("bulk_price", 0), "estimated_total_price": round(quantity * match.get("bulk_price", 0), 2)})
            remaining -= quantity
            if remaining <= 0:
                break
        fulfilled = required_quantity - max(remaining, 0)
        return {"status": "complete" if remaining <= 0 else "partial", "required_quantity": required_quantity, "fulfilled_quantity": fulfilled, "remaining_quantity": max(remaining, 0), "allocations": allocations}
