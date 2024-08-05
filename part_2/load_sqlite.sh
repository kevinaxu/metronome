.mode csv

CREATE TABLE IF NOT EXISTS "customer"(
    "id" TEXT PRIMARY KEY,
    "name" TEXT,
    "ingest_aliases" TEXT,
    "salesforce_account_id" TEXT,
    "billing_provider_type" TEXT,
    "billing_provider_customer_id" TEXT,
    "custom_fields" TEXT,
    "environment_type" TEXT,
    "created_at" TEXT,
    "updated_at" TEXT,
    "archived_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/customer.csv customer --skip 1

CREATE TABLE IF NOT EXISTS "events"(
    "transaction_id" TEXT, 
    "customer_id" TEXT, 
    "timestamp" TEXT, 
    "event_type" TEXT,
    "properties" JSON, 
    "environment_type" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/events.csv events --skip 1

CREATE TABLE IF NOT EXISTS "invoice"(
    "id" TEXT PRIMARY KEY, 
    "status" TEXT, 
    "total" DECIMAL(10,5), 
    "credit_type_id" TEXT,
    "credit_type_name" TEXT, 
    "customer_id" TEXT, 
    "plan_id" TEXT, 
    "plan_name" TEXT,
    "start_timestamp" TEXT, 
    "end_timestamp" TEXT, 
    "billing_provider_invoice_id" TEXT, 
    "billing_provider_invoice_external_status" TEXT,
    "invoice_label" TEXT, 
    "issued_at" TEXT, 
    "metadata" JSON, 
    "environment_type" TEXT,
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/invoice.csv invoice --skip 1


CREATE TABLE IF NOT EXISTS "line_item"(
    "id" TEXT PRIMARY KEY, 
    "invoice_id" TEXT, 
    "credit_grant_id" TEXT, 
    "credit_type_id" TEXT,
    "credit_type_name" TEXT, 
    "name" TEXT, 
    "quantity" INTEGER, 
    "total" DECIMAL(10,5), 
    "commit_id" TEXT, 
    "product_id" TEXT, 
    "group_value" TEXT, 
    "updated_at" TEXT
);
 .import /Users/Kevin/Dev/2024/metronome/sample_egress_data/line_item.csv line_item --skip 1 

 
CREATE TABLE IF NOT EXISTS "sub_line_item"(
    "id" TEXT PRIMARY KEY,
    "line_item_id" TEXT, 
    "name" TEXT, 
    "quantity" INTEGER, 
    "subtotal" DECIMAL(10,5), 
    "charge_id" TEXT, 
    "billable_metric_id" TEXT, 
    "billable_metric_name" TEXT,
    "tiers" JSON, 
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/sub_line_item.csv sub_line_item --skip 1 

CREATE TABLE IF NOT EXISTS "billable_metric"(
    "id" TEXT PRIMARY KEY,
    "aggregate" TEXT, 
    "aggregate_keys" JSON, 
    "environment_type" TEXT,
    "group_keys" JSON, 
    "name" TEXT, 
    "created_at" TEXT, 
    "archived_at" TEXT,
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/billable_metric.csv billable_metric --skip 1 

CREATE TABLE IF NOT EXISTS "product"(
    "id" TEXT, 
    "name" TEXT, 
    "description" TEXT, 
    "custom_fields" JSON,
    "created_at" TEXT, 
    "environment_type" TEXT, 
    "deprecated_at" TEXT, 
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/product.csv product --skip 1 

CREATE TABLE IF NOT EXISTS "plan"(
    "id" TEXT PRIMARY KEY, 
    "name" TEXT, 
    "description" TEXT, 
    "billing_frequency" TEXT,
    "starting_on" TEXT, 
    "custom_fields" JSON, 
    "environment_type" TEXT, 
    "created_at" TEXT,
    "deprecated_at" TEXT,
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/plan.csv plan --skip 1 

CREATE TABLE IF NOT EXISTS "plan_charge"(
    "id" TEXT PRIMARY KEY, 
    "charge_id" TEXT, 
    "name" TEXT, 
    "plan_id" TEXT,
    "product_id" TEXT, 
    "product_name" TEXT, 
    "billable_metric_id" TEXT, 
    "billable_metric_name" TEXT,
    "start_period" DECIMAL(10,5), 
    "credit_type_id" TEXT, 
    "credit_type_name" TEXT, 
    "charge_type" TEXT,
    "quantity" TEXT, 
    "environment_type" TEXT, 
    "custom_fields" JSON, 
    "updated_at" TEXT
);
.import /Users/Kevin/Dev/2024/metronome/sample_egress_data/plan_charge.csv plan_charge --skip 1 