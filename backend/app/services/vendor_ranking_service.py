from __future__ import annotations


class VendorRankingService:
    weights = {"price": 0.30, "distance": 0.20, "capacity": 0.20, "reliability": 0.15, "delivery": 0.15}

    def rank(self, matches: list[dict]) -> list[dict]:
        if not matches:
            return []
        prices = [item["capability"].get("bulkPrice", item["capability"].get("basePrice", 0)) for item in matches]
        distances = [item["distance_km"] for item in matches]
        max_capacity = max(item["capability"].get("maximumOrderCapacity", 0) for item in matches) or 1
        max_price, max_distance = max(prices) or 1, max(distances) or 1
        min_price, min_distance = min(prices), min(distances)
        for item in matches:
            vendor, capability = item["vendor"], item["capability"]
            price = capability.get("bulkPrice", capability.get("basePrice", 0))
            price_score = 100 if max_price == min_price else (max_price - price) / (max_price - min_price) * 100
            distance_score = 100 if max_distance == min_distance else (max_distance - item["distance_km"]) / (max_distance - min_distance) * 100
            capacity = capability.get("maximumOrderCapacity", 0)
            capacity_score = min(100, capacity / max_capacity * 100)
            delivery_score = max(0, 100 - capability.get("leadTimeDays", 30) * 5)
            item["overall_score"] = round(price_score * .30 + distance_score * .20 + capacity_score * .20 + vendor.get("reliability", 0) * .15 + delivery_score * .15, 1)
            item["bulk_price"] = price
        return sorted(matches, key=lambda item: item["overall_score"], reverse=True)