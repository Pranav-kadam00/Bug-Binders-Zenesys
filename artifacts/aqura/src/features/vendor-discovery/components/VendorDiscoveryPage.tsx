import { useState, type FormEvent } from "react";
import { Check, MapPin, Search, Sparkles, Truck } from "lucide-react";
import { Link } from "wouter";
import { useDiscoverBulkVendors } from "@workspace/api-client-react";
import { formatCurrency, formatIndianNumber } from "@/lib/currency";
import type { DiscoveryResponse } from "../types/vendorDiscovery.types";

export default function VendorDiscoveryPage() {
  const [form, setForm] = useState({
    productName: "",
    category: "",
    requiredQuantity: "",
    unit: "units",
    city: "Pune",
    initialRadiusKm: "10",
    maximumRadiusKm: "100",
    minimumVendorResults: "5",
    autoExpandRadius: true,
    allowPartialFulfillment: false,
  });
  const [result, setResult] = useState<DiscoveryResponse | null>(null);
  const [error, setError] = useState("");
  const discovery = useDiscoverBulkVendors();
  const loading = discovery.isPending;

  const update = (key: string, value: string | boolean) =>
    setForm((current) => ({ ...current, [key]: value }));

  const search = (event: FormEvent) => {
    event.preventDefault();
    setError("");
    discovery.mutate(
      {
        data: {
          productName: form.productName,
          category: form.category || undefined,
          requiredQuantity: Number(form.requiredQuantity),
          unit: form.unit,
          location: { city: form.city },
          initialRadiusKm: Number(form.initialRadiusKm),
          maximumRadiusKm: Number(form.maximumRadiusKm),
          minimumVendorResults: Number(form.minimumVendorResults),
          autoExpandRadius: form.autoExpandRadius,
          allowPartialFulfillment: form.allowPartialFulfillment,
          sortPreference: "recommended",
        },
      },
      {
        onSuccess: (response) => setResult(response as unknown as DiscoveryResponse),
        onError: (reason) =>
          setError(reason instanceof Error ? reason.message : "Unable to discover vendors"),
      },
    );
  };

  return (
    <div className="p-5 lg:p-10">
      {/* ── Header ── */}
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="mb-2 text-[11px] font-bold uppercase tracking-[.18em] text-primary">
            Expand your network
          </p>
          <h1 className="font-serif text-3xl font-bold tracking-tight text-foreground lg:text-[38px]">
            Discover vendors
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Find qualified bulk suppliers — AQURA searches your area and expands the radius
            automatically when needed.
          </p>
        </div>
        <Link href="/vendors" className="text-sm font-semibold text-muted-foreground">
          <MapPin className="mr-1 inline" size={14} /> Directory
        </Link>
      </div>

      {/* ── Search form ── */}
      <form
        onSubmit={search}
        className="rounded-2xl border border-primary/20 bg-primary/[.05] p-6 lg:p-8"
      >
        <div className="grid max-w-5xl gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <label className="lg:col-span-2">
            <span className="mb-2 block text-xs font-bold">Product or service</span>
            <input
              required
              value={form.productName}
              onChange={(e) => update("productName", e.target.value)}
              placeholder="e.g. Business laptop, Cement, Office chair"
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Category</span>
            <input
              value={form.category}
              onChange={(e) => update("category", e.target.value)}
              placeholder="IT Hardware"
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Quantity</span>
            <input
              required
              min="1"
              type="number"
              value={form.requiredQuantity}
              onChange={(e) => update("requiredQuantity", e.target.value)}
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Unit</span>
            <select
              value={form.unit}
              onChange={(e) => update("unit", e.target.value)}
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm"
            >
              <option>units</option>
              <option>bags</option>
              <option>boxes</option>
              <option>licenses</option>
              <option>each</option>
              <option>kg</option>
              <option>tonnes</option>
            </select>
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Delivery city or PIN</span>
            <input
              required
              value={form.city}
              onChange={(e) => update("city", e.target.value)}
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Initial radius (km)</span>
            <input
              min="1"
              type="number"
              value={form.initialRadiusKm}
              onChange={(e) => update("initialRadiusKm", e.target.value)}
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Maximum radius (km)</span>
            <input
              min="1"
              type="number"
              value={form.maximumRadiusKm}
              onChange={(e) => update("maximumRadiusKm", e.target.value)}
              className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary"
            />
          </label>
        </div>

        <div className="mt-5 flex flex-wrap items-center gap-5">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={form.autoExpandRadius}
              onChange={(e) => update("autoExpandRadius", e.target.checked)}
            />
            Auto-expand radius
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={form.allowPartialFulfillment}
              onChange={(e) => update("allowPartialFulfillment", e.target.checked)}
            />
            Allow partial fulfillment
          </label>
          <button
            disabled={loading}
            className="rounded-lg bg-primary px-5 py-2.5 text-sm font-bold text-primary-foreground disabled:opacity-60"
          >
            <Search className="mr-2 inline" size={16} />
            {loading ? "Searching…" : "Find suppliers"}
          </button>
        </div>
      </form>

      {/* ── Error ── */}
      {error && (
        <div className="mt-6 rounded-xl border border-destructive/20 bg-destructive/10 p-4 text-sm text-destructive">
          {error}
        </div>
      )}

      {/* ── Results ── */}
      {result && (
        <div className="mt-8 space-y-6">
          {/* Search summary card */}
          <div className="rounded-xl border border-border bg-card">
            <div className="border-b border-border px-5 py-4">
              <h2 className="font-serif text-lg font-bold">AQURA Smart Search</h2>
              <p className="mt-0.5 text-xs text-muted-foreground">
                {result.data.radius_search_summary.initial_radius_km} km →{" "}
                {result.data.radius_search_summary.final_radius_km} km
                {result.data.radius_search_summary.auto_expanded && (
                  <span className="ml-2 rounded-full bg-accent/20 px-2 py-0.5 text-[10px] font-bold text-accent-foreground">
                    Radius expanded
                  </span>
                )}
              </p>
            </div>
            <div className="p-5">
              <p className="text-sm leading-6">{result.data.insight}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {result.data.radius_levels.map((level) => (
                  <span
                    key={level.radius_km}
                    className="rounded-full border border-border bg-muted px-3 py-1.5 text-xs font-semibold"
                  >
                    {level.radius_km} km · {level.qualified_vendor_count} qualified
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Vendor cards */}
          <div className="flex items-center justify-between">
            <h2 className="font-serif text-xl font-bold">Qualified vendors</h2>
            <span className="text-xs text-muted-foreground">
              {result.data.vendors.length} found
            </span>
          </div>

          {result.data.vendors.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-border bg-card/60 px-6 py-14 text-center">
              <p className="font-serif text-xl font-bold">No vendors found</p>
              <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
                Try a broader product name, different category, or increase the maximum radius.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {result.data.vendors.map((vendor) => (
                <div key={vendor.id} className="rounded-xl border border-border bg-card p-5">
                  {/* Rank + name */}
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-[.14em] text-primary">
                        Rank #{vendor.rank}
                      </p>
                      <h3 className="mt-2 font-serif text-xl font-bold">{vendor.company_name}</h3>
                    </div>
                    {vendor.recommendation && (
                      <span className="rounded-full bg-primary/10 px-2 py-1 text-[10px] font-bold text-primary">
                        <Sparkles className="mr-1 inline" size={12} /> Recommended
                      </span>
                    )}
                  </div>

                  {/* Key metrics */}
                  <div className="mt-5 grid grid-cols-2 gap-4 text-sm">
                    <p>
                      <span className="block text-xs text-muted-foreground">Distance</span>
                      <MapPin className="mr-1 inline text-primary" size={13} />
                      {vendor.distance_km} km
                    </p>
                    <p>
                      <span className="block text-xs text-muted-foreground">Available qty</span>
                      {formatIndianNumber(vendor.available_quantity)} {form.unit}
                    </p>
                    <p>
                      <span className="block text-xs text-muted-foreground">
                        Bulk price / {form.unit}
                      </span>
                      <strong className="text-foreground">
                        {formatCurrency(vendor.bulk_price)}
                      </strong>
                    </p>
                    <p>
                      <span className="block text-xs text-muted-foreground">Lead time</span>
                      <Truck className="mr-1 inline text-primary" size={13} />
                      {vendor.lead_time_days} days
                    </p>
                  </div>

                  {/* Estimated total */}
                  <div className="mt-4 rounded-lg bg-primary/[.06] px-4 py-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">
                        Est. total ({formatIndianNumber(vendor.required_quantity ?? Number(form.requiredQuantity))} {form.unit})
                      </span>
                      <strong className="text-primary">
                        {formatCurrency(vendor.estimated_total_price)}
                      </strong>
                    </div>
                  </div>

                  {/* Score + reasons */}
                  <div className="mt-4 border-t border-border pt-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Overall score</span>
                      <strong className="text-primary">{vendor.overall_score} / 100</strong>
                    </div>
                    <div className="mt-3 space-y-1 text-xs text-muted-foreground">
                      {(vendor.recommendation_reasons ?? []).map((reason: string) => (
                        <p key={reason}>
                          <Check className="mr-1 inline text-primary" size={12} />
                          {reason}
                        </p>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
