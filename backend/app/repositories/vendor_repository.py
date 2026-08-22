from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import create_engine, text


class VendorRepository:
    """Reads discovery-ready vendor data from PostgreSQL when configured."""

    def __init__(self, database_url: str = "") -> None:
        self.engine = create_engine(database_url, pool_pre_ping=True) if database_url else None

    def discovery_vendors(self, fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self.engine is None:
            return fallback
        query = text("""
            SELECT v.id, v.company_name, v.category, concat_ws(', ', v.address, v.city, v.state) AS location, v.rating, v.status,
                   v.latitude, v.longitude, v.reliability, v.bulk_order_supported,
                   v.minimum_order_quantity, v.maximum_supply_capacity, v.delivery_radius_km,
                   c.product_name, c.product_category, c.minimum_order_quantity AS capability_minimum,
                   c.available_quantity, c.maximum_order_capacity, c.bulk_price, c.unit,
                   c.delivery_available, c.lead_time_days
            FROM vendors v
            JOIN vendor_product_capabilities c ON c.vendor_id = v.id
            WHERE v.status IN ('ACTIVE', 'VERIFIED', 'Preferred') AND c.is_active = true
        """)
        try:
            with self.engine.connect() as connection:
                rows = connection.execute(query).mappings().all()
            grouped: dict[int, dict[str, Any]] = {}
            for row in rows:
                vendor = grouped.setdefault(row["id"], {
                    "id": row["id"], "companyName": row["company_name"], "category": row["category"], "location": row["location"] or "", "rating": float(row["rating"] or 0), "status": row["status"], "latitude": float(row["latitude"]) if row["latitude"] is not None else None, "longitude": float(row["longitude"]) if row["longitude"] is not None else None, "reliability": float(row["reliability"] or 0), "bulkOrderSupported": row["bulk_order_supported"], "minimumOrderQuantity": float(row["minimum_order_quantity"] or 0), "maximumSupplyCapacity": float(row["maximum_supply_capacity"] or 0), "deliveryRadiusKm": float(row["delivery_radius_km"] or 0), "capabilities": [],
                })
                vendor["capabilities"].append({"productName": row["product_name"], "productCategory": row["product_category"], "minimumOrderQuantity": float(row["capability_minimum"]), "availableQuantity": float(row["available_quantity"]), "maximumOrderCapacity": float(row["maximum_order_capacity"]), "bulkPrice": float(row["bulk_price"]), "unit": row["unit"], "deliveryAvailable": row["delivery_available"], "leadTimeDays": row["lead_time_days"]})
            return list(grouped.values()) or fallback
        except Exception:
            return fallback
