CREATE TABLE "vendors" (
	"id" serial PRIMARY KEY NOT NULL,
	"company_name" text NOT NULL,
	"contact_person" text,
	"email" text,
	"phone" text,
	"address" text,
	"city" text,
	"state" text,
	"country" text,
	"pincode" text,
	"latitude" numeric(9, 6),
	"longitude" numeric(9, 6),
	"category" text NOT NULL,
	"website" text,
	"gst_number" text,
	"rating" numeric(3, 2),
	"status" text DEFAULT 'ACTIVE' NOT NULL,
	"minimum_order_quantity" numeric(14, 2) DEFAULT '0',
	"maximum_supply_capacity" numeric(14, 2) DEFAULT '0',
	"bulk_order_supported" boolean DEFAULT false NOT NULL,
	"delivery_radius_km" numeric(8, 2) DEFAULT '0',
	"average_bulk_price" numeric(14, 2),
	"serviceable_locations" jsonb DEFAULT '[]'::jsonb,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "vendor_product_capabilities" (
	"id" serial PRIMARY KEY NOT NULL,
	"vendor_id" integer NOT NULL,
	"product_name" text NOT NULL,
	"product_category" text NOT NULL,
	"minimum_order_quantity" numeric(14, 2) NOT NULL,
	"available_quantity" numeric(14, 2) NOT NULL,
	"maximum_order_capacity" numeric(14, 2) NOT NULL,
	"base_price" numeric(14, 2),
	"bulk_price" numeric(14, 2) NOT NULL,
	"unit" text NOT NULL,
	"delivery_available" boolean DEFAULT false NOT NULL,
	"lead_time_days" integer DEFAULT 0 NOT NULL,
	"is_active" boolean DEFAULT true NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "vendor_product_capabilities" ADD CONSTRAINT "vendor_product_capabilities_vendor_id_vendors_id_fk" FOREIGN KEY ("vendor_id") REFERENCES "public"."vendors"("id") ON DELETE no action ON UPDATE no action;