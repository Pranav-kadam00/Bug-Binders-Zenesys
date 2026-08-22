/**
 * AQURA — Centralized Currency & Tax Utilities
 * =============================================
 * All monetary display in the application must go through these helpers.
 * Default currency: Indian Rupee (INR), locale: en-IN
 *
 * Indian number formatting examples:
 *   ₹500       ₹5,000     ₹50,000
 *   ₹1,00,000  ₹10,00,000  ₹1,00,00,000
 */

const DEFAULT_CURRENCY = "INR";
const DEFAULT_LOCALE = "en-IN";

// ── Core formatter ────────────────────────────────────────────────────────────

/**
 * Format a number as Indian Rupee currency.
 * @example formatCurrency(100000) → "₹1,00,000"
 */
export function formatCurrency(
  amount: number | undefined | null,
  currency = DEFAULT_CURRENCY,
  locale = DEFAULT_LOCALE,
): string {
  if (amount == null || isNaN(amount)) return "₹0";
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount);
}

/**
 * Format with decimal places (for unit prices).
 * @example formatCurrencyDecimal(40800.50) → "₹40,800.50"
 */
export function formatCurrencyDecimal(
  amount: number | undefined | null,
  currency = DEFAULT_CURRENCY,
  locale = DEFAULT_LOCALE,
): string {
  if (amount == null || isNaN(amount)) return "₹0.00";
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format as Indian number (no currency symbol).
 * @example formatIndianNumber(1000000) → "10,00,000"
 */
export function formatIndianNumber(
  amount: number | undefined | null,
  locale = DEFAULT_LOCALE,
): string {
  if (amount == null || isNaN(amount)) return "0";
  return new Intl.NumberFormat(locale).format(amount);
}

/**
 * Compact format for large values.
 * @example formatCurrencyCompact(1000000) → "₹10L" or "₹1Cr"
 */
export function formatCurrencyCompact(amount: number | undefined | null): string {
  if (amount == null || isNaN(amount)) return "₹0";
  if (amount >= 10_000_000) return `₹${(amount / 10_000_000).toFixed(2)}Cr`;
  if (amount >= 100_000)    return `₹${(amount / 100_000).toFixed(2)}L`;
  if (amount >= 1_000)      return `₹${(amount / 1_000).toFixed(1)}K`;
  return `₹${amount}`;
}

// ── GST helpers ───────────────────────────────────────────────────────────────

export interface GSTBreakdown {
  subtotal: number;
  cgst: number;
  sgst: number;
  igst: number;
  totalTax: number;
  totalAmount: number;
  gstRate: number;
  currencyCode: string;
}

/**
 * Calculate GST breakdown (intra-state: CGST + SGST, inter-state: IGST).
 * @param subtotal  Pre-tax amount in INR
 * @param gstRate   GST rate percentage (default 18)
 * @param interState  If true, use IGST instead of CGST+SGST
 */
export function calculateGST(
  subtotal: number,
  gstRate = 18,
  interState = false,
): GSTBreakdown {
  const taxAmount = (subtotal * gstRate) / 100;
  const cgst = interState ? 0 : taxAmount / 2;
  const sgst = interState ? 0 : taxAmount / 2;
  const igst = interState ? taxAmount : 0;
  return {
    subtotal: round2(subtotal),
    cgst: round2(cgst),
    sgst: round2(sgst),
    igst: round2(igst),
    totalTax: round2(taxAmount),
    totalAmount: round2(subtotal + taxAmount),
    gstRate,
    currencyCode: DEFAULT_CURRENCY,
  };
}

/**
 * Calculate total including GST.
 */
export function calculateTotalWithTax(
  subtotal: number,
  gstRate = 18,
  interState = false,
): number {
  return calculateGST(subtotal, gstRate, interState).totalAmount;
}

/**
 * Parse a currency string like "₹1,00,000" back to a number.
 */
export function parseCurrencyInput(value: string): number {
  const cleaned = value.replace(/[₹,\s]/g, "");
  const num = parseFloat(cleaned);
  return isNaN(num) ? 0 : num;
}

// ── Internal ──────────────────────────────────────────────────────────────────

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}
