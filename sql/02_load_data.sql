-- ============================================================
-- OpsPulse Operational Intelligence
-- PostgreSQL Data Loading
-- ============================================================

SET search_path TO opspulse;

-- IMPORTANT:
-- Update the path below to your actual project folder.
-- PostgreSQL must be able to access these files.

COPY dim_date
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/dim_date.csv'
WITH (FORMAT csv, HEADER true);

COPY dim_customer
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/dim_customer.csv'
WITH (FORMAT csv, HEADER true);

COPY dim_product
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/dim_product.csv'
WITH (FORMAT csv, HEADER true);

COPY dim_employee
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/dim_employee.csv'
WITH (FORMAT csv, HEADER true);

COPY dim_location
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/dim_location.csv'
WITH (FORMAT csv, HEADER true);

COPY fact_operations
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/raw/fact_operations.csv'
WITH (FORMAT csv, HEADER true);

COPY fact_operation_stages
FROM 'C:/Users/rajpa/Downloads/OpsPulse Operational Intelligence/data/processed/fact_operation_stages.csv'
WITH (FORMAT csv, HEADER true);