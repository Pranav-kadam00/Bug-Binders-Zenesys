from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class GeocodingProvider(ABC):
    @abstractmethod
    async def geocode(self, location: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def reverse_geocode(self, latitude: float, longitude: float) -> dict[str, Any]:
        raise NotImplementedError
