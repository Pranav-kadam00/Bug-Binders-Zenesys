from __future__ import annotations

from .distance_service import DistanceService
from .location_service import LocationService
from .radius_expansion_service import RadiusExpansionService
from .vendor_capacity_service import VendorCapacityService
from .multi_vendor_fulfillment_service import MultiVendorFulfillmentService
from .vendor_ranking_service import VendorRankingService
from .vendor_recommendation_service import VendorRecommendationService


class VendorDiscoveryService:
    def __init__(self) -> None:
        self.location = LocationService()
        self.distance = DistanceService()
        self.radius = RadiusExpansionService()
        self.capacity = VendorCapacityService()
        self.fulfillment = MultiVendorFulfillmentService()
        self.ranking = VendorRankingService()
        self.recommendation = VendorRecommendationService()

    def discover(self, request, vendors: list[dict]) -> dict:
        buyer = self.location.resolve(request.location)
        qualified: list[dict] = []
        levels: list[dict] = []
        final_radius = request.initial_radius_km
        for radius in self.radius.levels(request.initial_radius_km, request.maximum_radius_km):
            for vendor in vendors:
                if any(item["vendor"]["id"] == vendor["id"] for item in qualified):
                    continue
                if vendor.get("latitude") is None or vendor.get("longitude") is None:
                    continue
                distance = self.distance.calculate_distance(buyer["latitude"], buyer["longitude"], vendor["latitude"], vendor["longitude"])
                if distance > radius:
                    continue
                match = self.capacity.qualify(vendor, request.product_name, request.category, request.required_quantity, distance, request.allow_partial_fulfillment)
                if match:
                    qualified.append({"vendor": vendor, **match})
            levels.append({"radius_km": radius, "qualified_vendor_count": len(qualified)})
            final_radius = radius
            if len(qualified) >= request.minimum_vendor_results or not request.auto_expand_radius:
                break
        ranked = self.ranking.rank(qualified)
        fulfillment = self.fulfillment.allocate(ranked, request.required_quantity) if request.allow_partial_fulfillment else None
        results = []
        for rank, match in enumerate(ranked, 1):
            vendor, capability = match["vendor"], match["capability"]
            results.append({"id": vendor["id"], "rank": rank, "company_name": vendor["companyName"], "distance_km": round(match["distance_km"], 1), "product_name": capability["productName"], "available_quantity": match["available_quantity"], "required_quantity": request.required_quantity, "bulk_order_supported": vendor["bulkOrderSupported"], "bulk_price": match["bulk_price"], "estimated_total_price": round(match["bulk_price"] * request.required_quantity, 2), "lead_time_days": capability.get("leadTimeDays", 0), "delivery_available": capability.get("deliveryAvailable", False), "rating": vendor.get("rating", 0), "reliability_score": vendor.get("reliability", 0), "overall_score": match["overall_score"], "recommendation": rank == 1, "recommendation_reasons": self.recommendation.explain(match, request.required_quantity)})
        return {"success": True, "message": "Qualified vendors discovered successfully", "data": {"search": {"product_name": request.product_name, "category": request.category, "required_quantity": request.required_quantity, "unit": request.unit}, "buyer_location": buyer, "radius_search_summary": {"initial_radius_km": request.initial_radius_km, "final_radius_km": final_radius, "maximum_radius_km": request.maximum_radius_km, "auto_expanded": final_radius > request.initial_radius_km}, "insight": f"Only {levels[0]['qualified_vendor_count']} qualified vendors were found within {request.initial_radius_km:g} km. Aqura expanded the search to {final_radius:g} km and found {len(results)} qualified vendors." if final_radius > request.initial_radius_km else f"{len(results)} qualified vendors were found within the initial search radius.", "vendors": results, "radius_levels": levels, "multi_vendor_fulfillment": fulfillment}}