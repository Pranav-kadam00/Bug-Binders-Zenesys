class VendorRecommendationService:
    @staticmethod
    def reasons(match: dict, required_quantity: float) -> list[str]:
        vendor = match["vendor"]
        reasons = []
        if match["distance_km"] <= 10:
            reasons.append("Located within 10 km of the delivery location")
        if match["available_quantity"] >= required_quantity:
            reasons.append("Can fulfill the complete order")
        if vendor.get("reliability", 0) >= 90:
            reasons.append("High reliability score")
        reasons.append("Competitive bulk pricing")
        return reasons

    def explain(self, match: dict, required_quantity: float) -> list[str]:
        return self.reasons(match, required_quantity)