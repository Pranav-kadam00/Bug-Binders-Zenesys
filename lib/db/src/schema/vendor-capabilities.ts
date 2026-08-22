import { createInsertSchema } from "drizzle-zod";
import { boolean, decimal, index, integer, pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";
import { vendorsTable } from "./vendors";
import { z } from "zod";

export const vendorProductCapabilitiesTable = pgTable("vendor_product_capabilities", {
  id: serial("id").primaryKey(), vendorId: integer("vendor_id").notNull().references(() => vendorsTable.id), productName: text("product_name").notNull(), productCategory: text("product_category").notNull(), minimumOrderQuantity: decimal("minimum_order_quantity", { precision: 14, scale: 2 }).notNull(), availableQuantity: decimal("available_quantity", { precision: 14, scale: 2 }).notNull(), maximumOrderCapacity: decimal("maximum_order_capacity", { precision: 14, scale: 2 }).notNull(), basePrice: decimal("base_price", { precision: 14, scale: 2 }), bulkPrice: decimal("bulk_price", { precision: 14, scale: 2 }).notNull(), unit: text("unit").notNull(), deliveryAvailable: boolean("delivery_available").notNull().default(false), leadTimeDays: integer("lead_time_days").notNull().default(0), isActive: boolean("is_active").notNull().default(true), createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(), updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
}, (table) => ({
  vendorIdx: index("vendor_capabilities_vendor_idx").on(table.vendorId),
  productCategoryIdx: index("vendor_capabilities_product_category_idx").on(table.productCategory),
  activeIdx: index("vendor_capabilities_active_idx").on(table.isActive),
}));

export const insertVendorProductCapabilitySchema = createInsertSchema(vendorProductCapabilitiesTable);
export type InsertVendorProductCapability = z.infer<typeof insertVendorProductCapabilitySchema>;
export type VendorProductCapability = typeof vendorProductCapabilitiesTable.$inferSelect;
