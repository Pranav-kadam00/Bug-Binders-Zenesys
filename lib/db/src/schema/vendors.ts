import { createInsertSchema } from "drizzle-zod";
import { boolean, decimal, index, integer, jsonb, pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";
import { z } from "zod";

export const vendorsTable = pgTable("vendors", {
  id: serial("id").primaryKey(),
  companyName: text("company_name").notNull(), contactPerson: text("contact_person"), email: text("email"), phone: text("phone"),
  address: text("address"), city: text("city"), state: text("state"), country: text("country"), pincode: text("pincode"),
  latitude: decimal("latitude", { precision: 9, scale: 6 }), longitude: decimal("longitude", { precision: 9, scale: 6 }),
  category: text("category").notNull(), website: text("website"), gstNumber: text("gst_number"), rating: decimal("rating", { precision: 3, scale: 2 }), reliability: decimal("reliability", { precision: 5, scale: 2 }), status: text("status").notNull().default("ACTIVE"),
  minimumOrderQuantity: decimal("minimum_order_quantity", { precision: 14, scale: 2 }).default("0"), maximumSupplyCapacity: decimal("maximum_supply_capacity", { precision: 14, scale: 2 }).default("0"), bulkOrderSupported: boolean("bulk_order_supported").notNull().default(false), deliveryRadiusKm: decimal("delivery_radius_km", { precision: 8, scale: 2 }).default("0"), averageBulkPrice: decimal("average_bulk_price", { precision: 14, scale: 2 }), serviceableLocations: jsonb("serviceable_locations").$type<string[]>().default([]), createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(), updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
}, (table) => ({
  categoryIdx: index("vendors_category_idx").on(table.category),
  statusIdx: index("vendors_status_idx").on(table.status),
  bulkIdx: index("vendors_bulk_order_supported_idx").on(table.bulkOrderSupported),
  latitudeIdx: index("vendors_latitude_idx").on(table.latitude),
  longitudeIdx: index("vendors_longitude_idx").on(table.longitude),
}));

export const insertVendorSchema = createInsertSchema(vendorsTable);
export type InsertVendor = z.infer<typeof insertVendorSchema>;
export type Vendor = typeof vendorsTable.$inferSelect;
