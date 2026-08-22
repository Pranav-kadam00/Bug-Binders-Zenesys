from __future__ import annotations

import os
from typing import Any, Optional

from .base import GeocodingProvider


class MapplsGeocodingProvider(GeocodingProvider):
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("MAP_API_KEY", "")

    async def geocode(self, location: str) -> dict[str, Any]:
        raise NotImplementedError("Mappls geocoding adapter is not enabled in this deployment")

    async def reverse_geocode(self, latitude: float, longitude: float) -> dict[str, Any]:
        raise NotImplementedError("Mappls reverse geocoding adapter is not enabled in this deployment")
