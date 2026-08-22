from __future__ import annotations

from typing import Any

from .base import GeocodingProvider


class MockGeocodingProvider(GeocodingProvider):
    async def geocode(self, location: str) -> dict[str, Any]:
        return {"address": location, "latitude": None, "longitude": None}

    async def reverse_geocode(self, latitude: float, longitude: float) -> dict[str, Any]:
        return {"latitude": latitude, "longitude": longitude, "address": f"{latitude:.4f}, {longitude:.4f}"}
