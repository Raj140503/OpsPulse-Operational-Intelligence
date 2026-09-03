-- ============================================================
-- OpsPulse Operational Intelligence
-- PostgreSQL Star Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS opspulse;

SET search_path TO opspulse;

-- ============================================================
-- DIMENSION TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    week INTEGER,
    day INTEGER,
    day_name VARCHAR(20),
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_segment VARCHAR(50),
    customer_region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    category VARCHAR(100),
    subcategory VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_employee (
    employee_id INTEGER PRIMARY KEY,
    department VARCHAR(100),
    experience_level VARCHAR(50),
    hire_date DATE
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id INTEGER PRIMARY KEY,
    region VARCHAR(50),
    facility_type VARCHAR(100),
    capacity NUMERIC(12,2)
);

-- ============================================================
-- FACT TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_operations (
    operation_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    customer_id INTEGER,
    product_id INTEGER,
    employee_id INTEGER,
    location_id INTEGER,
    order_date DATE,
    start_time TIMESTAMP,
    completion_time TIMESTAMP,
    expected_completion TIMESTAMP,
    status VARCHAR(50),
    quantity INTEGER,
    processing_time_hours NUMERIC(12,2),
    delay_minutes NUMERIC(12,2),
    sla_target_hours NUMERIC(12,2),
    sla_breached BOOLEAN,
    workload NUMERIC(12,2),
    cost NUMERIC(14,2),
    quality_score NUMERIC(8,2),

    CONSTRAINT fk_operations_customer
        FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    CONSTRAINT fk_operations_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    CONSTRAINT fk_operations_employee
        FOREIGN KEY (employee_id)
        REFERENCES dim_employee(employee_id),

    CONSTRAINT fk_operations_location
        FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id)
);

-- ============================================================
-- STAGE FACT TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_operation_stages (
    operation_id BIGINT,
    stage_id INTEGER,
    stage_name VARCHAR(100),
    stage_sequence INTEGER,
    stage_start_time TIMESTAMP,
    stage_end_time TIMESTAMP,
    stage_duration_minutes NUMERIC(12,2),
    target_time_minutes NUMERIC(12,2),
    stage_variance_minutes NUMERIC(12,2),
    stage_status VARCHAR(50),

    PRIMARY KEY (operation_id, stage_id),

    CONSTRAINT fk_stage_operation
        FOREIGN KEY (operation_id)
        REFERENCES fact_operations(operation_id)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_operations_order_date
    ON fact_operations(order_date);

CREATE INDEX IF NOT EXISTS idx_operations_employee
    ON fact_operations(employee_id);

CREATE INDEX IF NOT EXISTS idx_operations_product
    ON fact_operations(product_id);

CREATE INDEX IF NOT EXISTS idx_operations_location
    ON fact_operations(location_id);

CREATE INDEX IF NOT EXISTS idx_stages_stage_name
    ON fact_operation_stages(stage_name);

CREATE INDEX IF NOT EXISTS idx_stages_operation
    ON fact_operation_stages(operation_id);