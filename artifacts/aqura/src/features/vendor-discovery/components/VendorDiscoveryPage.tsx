import { useState, type FormEvent } from "react";
import {
  Check, ChevronDown, ChevronUp, Filter, Globe, Loader2,
  MapPin, Search, Sparkles, Star, Truck, Zap, X, SlidersHorizontal,
  Award, Clock, Package, BarChart3, ArrowRight, Info,
} from "lucide-react";
import { Link } from "wouter";
import { useDiscoverBulkVendors } from "@workspace/api-client-react";
import type { DiscoveryResponse } from "../types/vendorDiscovery.types";

// ── Radius options ─────────────────────────────────────────────────────────────
const RADIUS_OPTIONS: { label: string; km: number | null }[] = [
  { label: "10 km",    km: 10   },
  { label: "20 km",    km: 20   },
  { label: "30 km",    km: 30   },
  { label: "50 km",    km: 50   },
  { label: "100 km",   km: 100  },
  { label: "Anywhere", km: null },
];

// ── Sort options ───────────────────────────────────────────────────────────────
const SORT_OPTIONS = [
  { value: "recommended", label: "Recommended",     icon: Sparkles  },
  { value: "price",       label: "Best price",      icon: BarChart3 },
  { value: "distance",    label: "Nearest first",   icon: MapPin    },
  { value: "delivery",    label: "Fastest delivery",icon: Truck     },
  { value: "reliability", label: "Most reliable",   icon: Award     },
] as const;

// ── Category chips ─────────────────────────────────────────────────────────────
const CATEGORY_CHIPS = [
  "IT Hardware","Office Supplies","Infrastructure","Logistics",
  "Software / SaaS","Facilities","Equipment","Professional Services",
];

// ── Unit options ───────────────────────────────────────────────────────────────
const UNIT_OPTIONS = ["units","bags","boxes","licenses","each","kg","litres","sets"];

// ── Helpers ────────────────────────────────────────────────────────────────────
const scoreColor = (s: number) =>
  s >= 85 ? "text-emerald-600" : s >= 70 ? "text-primary" : "text-amber-600";
const scoreBg = (s: number) =>
  s >= 85 ? "bg-emerald-500" : s >= 70 ? "bg-primary" : "bg-amber-500";

function ScoreBar({ value }: { value: number }) {
  const pct = Math.min(100, value);
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
      <div
        className={`h-full rounded-full transition-all duration-700 ${scoreBg(value)}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

// ── Animated radius ring visualiser ───────────────────────────────────────────
function RadiusRing({ km }: { km: number | null }) {
  const rings = [0.3, 0.6, 1.0];
  return (
    <div className="relative flex h-28 w-28 shrink-0 items-center justify-center">
      {rings.map((scale, i) => (
        <div
          key={i}
          className={`absolute rounded-full border transition-all duration-500 ${
            i === 2 ? "border-primary/60 bg-primary/10" : "border-primary/20"
          }`}
          style={{ width: `${scale * 100}%`, height: `${scale * 100}%` }}
        />
      ))}
      <div className="z-10 grid h-6 w-6 place-items-center rounded-full bg-primary shadow-md shadow-primary/30">
        {km === null
          ? <Globe size={11} className="text-primary-foreground" />
          : <MapPin size={11} className="text-primary-foreground" />}
      </div>
      <span className="absolute bottom-0 right-0 rounded-full bg-primary/10 px-1.5 py-0.5 text-[10px] font-bold text-primary">
        {km === null ? "∞" : `${km} km`}
      </span>
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────
export default function VendorDiscoveryPage() {
  const [radiusKm, setRadiusKm] = useState<number | null>(30);
  const [sort, setSort]         = useState<typeof SORT_OPTIONS[number]["value"]>("recommended");
  const [showAdv, setShowAdv]   = useState(false);
  const [form, setForm] = useState({
    productName: "", category: "", requiredQuantity: "",
    unit: "units", city: "Pune",
    minimumVendorResults: "5",
    autoExpandRadius: true,
    allowPartialFulfillment: false,
  });
  const [result, setResult] = useState<DiscoveryResponse | null>(null);
  const [error,  setError]  = useState("");

  const discovery = useDiscoverBulkVendors();
  const loading   = discovery.isPending;
  const update    = (k: string, v: string | boolean) => setForm(p => ({ ...p, [k]: v }));

  const effectiveRadius = radiusKm ?? 5000;

  const handleSearch = (e: FormEvent) => {
    e.preventDefault(); setError("");
    discovery.mutate(
      { data: {
          productName: form.productName,
          category: form.category || undefined,
          requiredQuantity: Number(form.requiredQuantity) || 1,
          unit: form.unit,
          location: { city: form.city },
          initialRadiusKm: effectiveRadius,
          maximumRadiusKm: radiusKm === null ? 5000 : Math.max(effectiveRadius * 2, 200),
          minimumVendorResults: Number(form.minimumVendorResults),
          autoExpandRadius: form.autoExpandRadius,
          allowPartialFulfillment: form.allowPartialFulfillment,
          sortPreference: sort,
      }},
      {
        onSuccess: r => setResult(r as unknown as DiscoveryResponse),
        onError:   r => setError(r instanceof Error ? r.message : "Unable to discover vendors"),
      }
    );
  };

  const vendors = result?.data?.vendors ?? [];
  const summary = result?.data?.radius_search_summary;
  const levels  = result?.data?.radius_levels ?? [];

  return (
    <div className="p-5 lg:p-10">
      {/* Page header */}
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="mb-2 text-[11px] font-bold uppercase tracking-[.18em] text-primary">Expand your network</p>
          <h1 className="font-serif text-3xl font-bold tracking-tight text-foreground lg:text-[38px]">Discover vendors</h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Find capable partners within your reach — choose a radius or search anywhere.
          </p>
        </div>
        <Link href="/vendors" className="text-sm font-semibold text-muted-foreground hover:text-foreground">
          <MapPin className="mr-1 inline" size={14} /> Directory
        </Link>
      </div>

      {/* Discovery form */}
      <form onSubmit={handleSearch} className="rounded-2xl border border-primary/20 bg-primary/[.04] p-6 lg:p-8">

        {/* Row 1 – product + city + qty */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <label className="lg:col-span-2">
            <span className="mb-2 block text-xs font-bold">Product or service</span>
            <div className="relative">
              <Search className="absolute left-3 top-3 text-muted-foreground" size={16} />
              <input required value={form.productName} onChange={e => update("productName", e.target.value)}
                placeholder="e.g. Business laptops, cooling units…"
                className="h-11 w-full rounded-lg border border-input bg-card pl-9 pr-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/15" />
            </div>
          </label>
          <label>
            <span className="mb-2 block text-xs font-bold">Delivery city / PIN</span>
            <div className="relative">
              <MapPin className="absolute left-3 top-3 text-muted-foreground" size={16} />
              <input required value={form.city} onChange={e => update("city", e.target.value)}
                className="h-11 w-full rounded-lg border border-input bg-card pl-9 pr-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/15" />
            </div>
          </label>
          <div className="flex gap-2">
            <label className="flex-1">
              <span className="mb-2 block text-xs font-bold">Quantity</span>
              <input min="1" type="number" value={form.requiredQuantity}
                onChange={e => update("requiredQuantity", e.target.value)} placeholder="Qty"
                className="h-11 w-full rounded-lg border border-input bg-card px-3 text-sm outline-none focus:border-primary" />
            </label>
            <label className="w-28">
              <span className="mb-2 block text-xs font-bold">Unit</span>
              <select value={form.unit} onChange={e => update("unit", e.target.value)}
                className="h-11 w-full rounded-lg border border-input bg-card px-2 text-sm">
                {UNIT_OPTIONS.map(u => <option key={u}>{u}</option>)}
              </select>
            </label>
          </div>
        </div>

        {/* Category chips */}
        <div className="mt-5">
          <p className="mb-2.5 text-xs font-bold">Category</p>
          <div className="flex flex-wrap gap-2">
            {CATEGORY_CHIPS.map(cat => (
              <button key={cat} type="button"
                onClick={() => update("category", form.category === cat ? "" : cat)}
                className={`rounded-full border px-3 py-1.5 text-[11px] font-semibold transition-colors ${
                  form.category === cat
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border bg-card text-muted-foreground hover:border-primary/50 hover:text-foreground"
                }`}>
                {cat}
              </button>
            ))}
            {form.category && !CATEGORY_CHIPS.includes(form.category) && (
              <span className="flex items-center gap-1 rounded-full border border-primary bg-primary/10 px-3 py-1.5 text-[11px] font-semibold text-primary">
                {form.category}
                <button type="button" onClick={() => update("category", "")}><X size={11} /></button>
              </span>
            )}
          </div>
          <input value={form.category} onChange={e => update("category", e.target.value)}
            placeholder="Or type a custom category…"
            className="mt-2 h-9 w-full max-w-xs rounded-lg border border-input bg-card px-3 text-xs outline-none focus:border-primary" />
        </div>

        {/* Radius selector */}
        <div className="mt-6">
          <p className="mb-3 text-xs font-bold">Search radius</p>
          <div className="flex flex-wrap items-center gap-4">
            <RadiusRing km={radiusKm} />
            <div className="flex flex-wrap gap-2">
              {RADIUS_OPTIONS.map(({ label, km }) => {
                const active = radiusKm === km;
                const isAnywhere = km === null;
                return (
                  <button key={label} type="button" onClick={() => setRadiusKm(km)}
                    className={`flex items-center gap-1.5 rounded-full border px-4 py-2 text-[12px] font-bold transition-all duration-150 ${
                      active
                        ? "border-primary bg-primary text-primary-foreground shadow-md shadow-primary/20"
                        : "border-border bg-card text-muted-foreground hover:border-primary/50 hover:text-primary"
                    }`}>
                    {isAnywhere ? <Globe size={13} /> : <MapPin size={13} />}
                    {label}
                  </button>
                );
              })}
            </div>
          </div>
          <p className="mt-2 text-[11px] text-muted-foreground">
            <Info size={11} className="mr-1 inline" />
            {radiusKm !== null
              ? <>Searching within <strong>{radiusKm} km</strong> of {form.city || "your city"}.</>
              : <><strong>Anywhere</strong> — global search with no radius restriction.</>}
            {" "}Auto-expand is {form.autoExpandRadius ? "on" : "off"}.
          </p>
        </div>

        {/* Sort preference */}
        <div className="mt-5">
          <p className="mb-3 text-xs font-bold">Sort preference</p>
          <div className="flex flex-wrap gap-2">
            {SORT_OPTIONS.map(({ value, label, icon: Icon }) => (
              <button key={value} type="button" onClick={() => setSort(value)}
                className={`flex items-center gap-1.5 rounded-lg border px-3 py-2 text-xs font-semibold transition-all ${
                  sort === value
                    ? "border-primary/40 bg-primary/10 text-primary"
                    : "border-border bg-card text-muted-foreground hover:border-primary/30 hover:text-foreground"
                }`}>
                <Icon size={13} />{label}
              </button>
            ))}
          </div>
        </div>

        {/* Advanced options */}
        <div className="mt-5">
          <button type="button" onClick={() => setShowAdv(v => !v)}
            className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground hover:text-foreground">
            <SlidersHorizontal size={13} /> Advanced options
            {showAdv ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
          </button>
          {showAdv && (
            <div className="mt-4 grid gap-4 rounded-xl border border-border bg-card p-4 sm:grid-cols-3">
              <label>
                <span className="mb-1.5 block text-[11px] font-bold">Min. vendor results</span>
                <input type="number" min="1" max="20" value={form.minimumVendorResults}
                  onChange={e => update("minimumVendorResults", e.target.value)}
                  className="h-9 w-full rounded-lg border border-input bg-background px-3 text-xs" />
              </label>
              <label className="flex cursor-pointer items-start gap-3 pt-5">
                <input type="checkbox" checked={form.autoExpandRadius}
                  onChange={e => update("autoExpandRadius", e.target.checked)}
                  className="mt-0.5 h-4 w-4 accent-[hsl(var(--primary))]" />
                <span className="text-xs leading-5">
                  <strong className="block text-foreground">Auto-expand radius</strong>
                  Widens search if too few vendors found
                </span>
              </label>
              <label className="flex cursor-pointer items-start gap-3 pt-5">
                <input type="checkbox" checked={form.allowPartialFulfillment}
                  onChange={e => update("allowPartialFulfillment", e.target.checked)}
                  className="mt-0.5 h-4 w-4 accent-[hsl(var(--primary))]" />
                <span className="text-xs leading-5">
                  <strong className="block text-foreground">Partial fulfillment</strong>
                  Allow vendors who can't fill full quantity
                </span>
              </label>
            </div>
          )}
        </div>

        {/* Submit row */}
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <button type="submit" disabled={loading}
            className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-bold text-primary-foreground shadow-md shadow-primary/20 hover:-translate-y-0.5 disabled:opacity-60">
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
            {loading ? "Searching…" : "Find suppliers"}
          </button>
          {result && (
            <button type="button" onClick={() => { setResult(null); setError(""); }}
              className="rounded-lg border border-border px-4 py-3 text-sm font-semibold text-muted-foreground hover:bg-muted">
              <X size={15} className="mr-1 inline" /> Clear
            </button>
          )}
          <span className="text-xs text-muted-foreground">
            {radiusKm !== null ? `Within ${radiusKm} km` : "Global"} · {sort}
          </span>
        </div>
      </form>

      {/* Error */}
      {error && (
        <div className="mt-6 rounded-xl border border-destructive/20 bg-destructive/10 p-4 text-sm text-destructive">{error}</div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-8 space-y-8">

          {/* Summary */}
          <div className="rounded-xl border border-border bg-card p-5">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[.15em] text-primary">AQURA Smart Search · radius insight</p>
                <p className="mt-2 max-w-2xl text-sm leading-6">{result.data.insight}</p>
              </div>
              {summary && (
                <div className="flex items-center gap-3 rounded-xl border border-primary/20 bg-primary/5 px-4 py-3 text-center">
                  <div>
                    <p className="font-mono text-2xl font-bold text-primary">{summary.initial_radius_km}</p>
                    <p className="text-[10px] text-muted-foreground">initial km</p>
                  </div>
                  <ArrowRight size={16} className="text-primary" />
                  <div>
                    <p className="font-mono text-2xl font-bold">{summary.final_radius_km}</p>
                    <p className="text-[10px] text-muted-foreground">final km</p>
                  </div>
                  {summary.auto_expanded && (
                    <span className="ml-2 rounded-full bg-accent/15 px-2 py-1 text-[10px] font-bold">Auto-expanded</span>
                  )}
                </div>
              )}
            </div>
            {levels.length > 0 && (
              <div className="mt-5 flex flex-wrap gap-2">
                {levels.map(lvl => (
                  <span key={lvl.radius_km}
                    className={`flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-semibold ${
                      lvl.radius_km === summary?.final_radius_km
                        ? "border-primary/40 bg-primary/10 text-primary"
                        : "border-border bg-muted text-muted-foreground"
                    }`}>
                    <MapPin size={11} />{lvl.radius_km} km
                    <span className="rounded-full bg-background px-1.5 py-0.5 text-[10px] font-bold">{lvl.qualified_vendor_count} found</span>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Vendor cards */}
          <div>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="font-serif text-2xl font-bold">Qualified vendors</h2>
                <p className="mt-1 text-xs text-muted-foreground">
                  {vendors.length} supplier{vendors.length !== 1 ? "s" : ""} found · sorted by {sort}
                </p>
              </div>
              <div className="flex items-center gap-1 rounded-lg border border-border bg-card px-3 py-2 text-xs font-semibold text-muted-foreground">
                <Filter size={13} /> {vendors.length} results
              </div>
            </div>

            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {vendors.map((vendor: Record<string, any>) => (
                <div key={vendor.id}
                  className={`flex flex-col rounded-2xl border bg-card p-5 transition-shadow hover:shadow-lg hover:shadow-primary/5 ${
                    vendor.recommendation ? "border-primary/35 ring-1 ring-primary/15" : "border-border"
                  }`}>

                  {/* Top */}
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-[10px] font-bold uppercase tracking-[.14em] text-primary">Rank #{vendor.rank}</p>
                      <h3 className="mt-2 font-serif text-xl font-bold leading-tight">{vendor.company_name}</h3>
                    </div>
                    {vendor.recommendation
                      ? <span className="flex items-center gap-1 rounded-full bg-primary/10 px-2.5 py-1 text-[10px] font-bold text-primary"><Sparkles size={11} /> Recommended</span>
                      : <span className="rounded-full border border-border bg-muted px-2.5 py-1 text-[10px] font-semibold text-muted-foreground">Qualified</span>}
                  </div>

                  {/* Quick stats */}
                  <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                    {[
                      { icon: MapPin,   label: "Distance", val: `${vendor.distance_km} km` },
                      { icon: Truck,    label: "Delivery",  val: `${vendor.lead_time_days} days` },
                      { icon: Package,  label: "Capacity",  val: `${vendor.available_quantity} ${form.unit}` },
                      { icon: Zap,      label: "Bulk price",val: `${vendor.bulk_price} / ${form.unit}` },
                    ].map(({ icon: Icon, label, val }) => (
                      <div key={label} className="rounded-lg bg-muted/60 p-3">
                        <p className="flex items-center gap-1 text-[10px] text-muted-foreground"><Icon size={10} />{label}</p>
                        <p className="mt-1 font-mono text-base font-bold">{val}</p>
                      </div>
                    ))}
                  </div>

                  {/* Score bars */}
                  <div className="mt-4 border-t border-border pt-4 space-y-2.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-muted-foreground">Overall score</span>
                      <strong className={`font-mono text-sm ${scoreColor(vendor.overall_score)}`}>{vendor.overall_score} / 100</strong>
                    </div>
                    <ScoreBar value={vendor.overall_score} />
                    {[
                      { label: "Reliability",    v: vendor.reliability_score ?? vendor.reliability ?? 0 },
                      { label: "Price",          v: vendor.price_score ?? vendor.pricing ?? 0 },
                      { label: "Delivery speed", v: vendor.delivery_score ?? 0 },
                    ].map(({ label, v }) => v > 0 && (
                      <div key={label} className="flex items-center gap-3 text-[11px]">
                        <span className="w-24 shrink-0 text-muted-foreground">{label}</span>
                        <div className="flex-1"><ScoreBar value={v} /></div>
                        <span className={`w-8 text-right font-mono font-semibold ${scoreColor(v)}`}>{v}</span>
                      </div>
                    ))}
                  </div>

                  {/* Reasons */}
                  {vendor.recommendation_reasons?.length > 0 && (
                    <div className="mt-4 space-y-1 border-t border-border pt-3">
                      {vendor.recommendation_reasons.slice(0, 3).map((r: string) => (
                        <p key={r} className="flex items-start gap-1.5 text-[11px] text-muted-foreground">
                          <Check size={11} className="mt-0.5 shrink-0 text-primary" />{r}
                        </p>
                      ))}
                    </div>
                  )}

                  {/* Star rating */}
                  {vendor.rating != null && (
                    <div className="mt-3 flex items-center gap-1 text-xs text-amber-500">
                      <Star size={12} fill="currentColor" />
                      <span className="font-mono font-bold">{Number(vendor.rating).toFixed(1)}</span>
                      <span className="text-muted-foreground">/ 5</span>
                    </div>
                  )}

                  {/* CTA */}
                  <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-primary/30 py-2.5 text-xs font-bold text-primary hover:bg-primary hover:text-primary-foreground transition-colors">
                    Request quote <ArrowRight size={13} />
                  </button>
                </div>
              ))}
            </div>

            {vendors.length === 0 && (
              <div className="rounded-2xl border border-dashed border-border bg-card/60 px-6 py-14 text-center">
                <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-2xl bg-primary/10 text-primary">
                  <Search size={22} />
                </div>
                <h3 className="font-serif text-xl font-bold">No vendors found</h3>
                <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
                  Try a larger radius, enable auto-expand, or broaden the category.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
