import unittest

from backend.app.services.distance_service import DistanceService
from backend.app.services.multi_vendor_fulfillment_service import MultiVendorFulfillmentService
from backend.app.services.radius_expansion_service import RadiusExpansionService
from backend.app.services.vendor_capacity_service import VendorCapacityService
from backend.app.services.vendor_ranking_service import VendorRankingService


def match(vendor_id, score, available, maximum, price=100, minimum=1):
    vendor = {"id": vendor_id, "companyName": f"Vendor {vendor_id}", "status": "ACTIVE", "bulkOrderSupported": True, "deliveryRadiusKm": 100, "reliability": 90}
    capability = {"productName": "Cement", "availableQuantity": available, "maximumOrderCapacity": maximum, "minimumOrderQuantity": minimum, "bulkPrice": price, "deliveryAvailable": True, "leadTimeDays": 2}
    return {"vendor": vendor, "capability": capability, "available_quantity": available, "distance_km": 5, "overall_score": score, "bulk_price": price}


class VendorDiscoveryTests(unittest.TestCase):
    def test_haversine_distance_and_progressive_radius(self):
        distance = DistanceService.calculate_distance(18.5204, 73.8567, 18.56, 73.9)
        self.assertAlmostEqual(distance, 6.34, places=1)
        self.assertEqual(RadiusExpansionService().levels(10, 100), [10, 25, 50, 100])

    def test_capacity_rejects_insufficient_quantity_and_delivery(self):
        service = VendorCapacityService()
        vendor = {"status": "ACTIVE", "bulkOrderSupported": True, "deliveryRadiusKm": 5, "capabilities": [{"productName": "Cement", "availableQuantity": 10, "maximumOrderCapacity": 10, "minimumOrderQuantity": 2, "deliveryAvailable": True}]}
        self.assertIsNone(service.qualify(vendor, "Cement", None, 11, 1))
        self.assertIsNone(service.qualify(vendor, "Cement", None, 5, 6))
        self.assertIsNotNone(service.qualify(vendor, "Cement", None, 5, 1))

    def test_ranking_orders_by_score(self):
        ranked = VendorRankingService().rank([match(1, 1, 100, 100), match(2, 1, 100, 100, price=80)])
        self.assertEqual(ranked[0]["vendor"]["id"], 2)
        self.assertGreaterEqual(ranked[0]["overall_score"], 0)
        self.assertLessEqual(ranked[0]["overall_score"], 100)

    def test_partial_fulfillment_allocates_across_vendors(self):
        result = MultiVendorFulfillmentService().allocate([match(1, 2, 40, 40), match(2, 1, 60, 60)], 100)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["fulfilled_quantity"], 100)
        self.assertEqual(len(result["allocations"]), 2)


if __name__ == "__main__":
    unittest.main()
