from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class DiscoveryLocation(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def has_coordinates_or_search_text(self) -> "DiscoveryLocation":
        has_coordinates = self.latitude is not None and self.longitude is not None
        if not has_coordinates and not any((self.address, self.city, self.pincode)):
            raise ValueError("location needs coordinates, an address, a city, or a pincode")
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be provided together")
        return self


class VendorDiscoveryRequest(BaseModel):
    product_name: str = Field(min_length=1, alias="productName")
    category: Optional[str] = None
    required_quantity: float = Field(gt=0, alias="requiredQuantity")
    unit: str = Field(min_length=1)
    location: DiscoveryLocation
    initial_radius_km: float = Field(default=10, gt=0, alias="initialRadiusKm")
    maximum_radius_km: float = Field(default=100, gt=0, le=500, alias="maximumRadiusKm")
    auto_expand_radius: bool = Field(default=True, alias="autoExpandRadius")
    minimum_vendor_results: int = Field(default=5, ge=1, le=100, alias="minimumVendorResults")
    allow_partial_fulfillment: bool = Field(default=False, alias="allowPartialFulfillment")
    sort_preference: Literal["recommended", "price", "distance", "delivery", "reliability"] = Field(default="recommended", alias="sortPreference")

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def valid_radius(self) -> "VendorDiscoveryRequest":
        if self.maximum_radius_km < self.initial_radius_km:
            raise ValueError("maximumRadiusKm must be greater than or equal to initialRadiusKm")
        return self