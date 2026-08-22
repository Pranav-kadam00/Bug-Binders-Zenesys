from __future__ import annotations

import os
from typing import Any


class LocationService:
    _known_locations = {
        "pune": (18.5204, 73.8567),
        "411001": (18.5204, 73.8567),
        "mumbai": (19.0760, 72.8777),
        "bengaluru": (12.9716, 77.5946),
        "hyderabad": (17.3850, 78.4867),
        "chennai": (13.0827, 80.2707),
    }

    def resolve(self, location: Any) -> dict[str, Any]:
        if location.latitude is not None and location.longitude is not None:
            return {"latitude": location.latitude, "longitude": location.longitude, "address": location.address or location.city or location.pincode}
        text = " ".join(filter(None, (location.address, location.city, location.pincode))).lower()
        for key, coordinates in self._known_locations.items():
            if key in text:
                return {"latitude": coordinates[0], "longitude": coordinates[1], "address": location.address or location.city or location.pincode}
        raise ValueError("Unable to determine coordinates for the selected location")

    @staticmethod
    def provider_name() -> str:
        return os.getenv("MAP_PROVIDER", "mock")