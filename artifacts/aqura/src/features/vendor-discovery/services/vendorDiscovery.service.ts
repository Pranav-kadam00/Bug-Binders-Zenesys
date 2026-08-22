import type { DiscoveryRequest, DiscoveryResponse } from "../types/vendorDiscovery.types";

export async function discoverBulkVendors(request: DiscoveryRequest): Promise<DiscoveryResponse> {
  const response = await fetch("/api/v1/vendors/bulk-discover", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Unable to discover vendors");
  return response.json();
}
