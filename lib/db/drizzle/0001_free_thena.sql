CREATE INDEX "vendors_category_idx" ON "vendors" USING btree ("category");--> statement-breakpoint
CREATE INDEX "vendors_status_idx" ON "vendors" USING btree ("status");--> statement-breakpoint
CREATE INDEX "vendors_bulk_order_supported_idx" ON "vendors" USING btree ("bulk_order_supported");--> statement-breakpoint
CREATE INDEX "vendors_latitude_idx" ON "vendors" USING btree ("latitude");--> statement-breakpoint
CREATE INDEX "vendors_longitude_idx" ON "vendors" USING btree ("longitude");--> statement-breakpoint
CREATE INDEX "vendor_capabilities_vendor_idx" ON "vendor_product_capabilities" USING btree ("vendor_id");--> statement-breakpoint
CREATE INDEX "vendor_capabilities_product_category_idx" ON "vendor_product_capabilities" USING btree ("product_category");--> statement-breakpoint
CREATE INDEX "vendor_capabilities_active_idx" ON "vendor_product_capabilities" USING btree ("is_active");