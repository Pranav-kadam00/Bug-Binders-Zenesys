export type DiscoveryRequest = {
  productName: string;
  category?: string;
  requiredQuantity: number;
  unit: string;
  location: { city?: string; pincode?: string; address?: string; latitude?: number; longitude?: number };
  initialRadiusKm: number;
  maximumRadiusKm: number;
  autoExpandRadius: boolean;
  minimumVendorResults: number;
  allowPartialFulfillment: boolean;
  sortPreference: "recommended" | "price" | "distance" | "delivery" | "reliability";
};

export type DiscoveryResponse = {
  success: boolean;
  message: string;
  data: {
    insight: string;
    radius_search_summary: { initial_radius_km: number; final_radius_km: number; maximum_radius_km: number; auto_expanded: boolean };
    vendors: Array<Record<string, any>>;
    radius_levels: Array<{ radius_km: number; qualified_vendor_count: number }>;
  };
};
