from __future__ import annotations

from typing import Optional

class VendorCapacityService:
    def qualify(self, vendor: dict, product_name: str, category: Optional[str], quantity: float, distance_km: float, allow_partial: bool = False) -> Optional[dict]:
        capabilities = vendor.get("capabilities", [])
        capability = next((item for item in capabilities if item["productName"].lower() == product_name.lower()), None)
        if capability is None and category and vendor.get("category", "").lower() == category.lower():
            capability = vendor.get("defaultCapability")
        if capability is None or vendor.get("status", "").lower() not in {"active", "preferred", "verified"} or not vendor.get("bulkOrderSupported", False):
            return None
        available = capability.get("availableQuantity", 0)
        max_capacity = capability.get("maximumOrderCapacity", available)
        if not allow_partial and (available < quantity or max_capacity < quantity):
            return None
        if quantity < capability.get("minimumOrderQuantity", vendor.get("minimumOrderQuantity", 0)):
            return None
        delivery_radius = vendor.get("deliveryRadiusKm", 0)
        if distance_km > delivery_radius or not capability.get("deliveryAvailable", False):
            return None
        return {"capability": capability, "available_quantity": available, "fulfillment_quantity": min(available, quantity), "distance_km": distance_km}