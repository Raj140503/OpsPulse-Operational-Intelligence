-- ============================================================
-- OpsPulse — Power BI Analytical Views
-- ============================================================

SET search_path TO opspulse;

-- 1. Operations overview
CREATE OR REPLACE VIEW vw_operations_overview AS
SELECT
    f.operation_id,
    f.order_id,
    f.order_date,
    f.status,
    f.quantity,
    f.processing_time_hours,
    f.delay_minutes,
    f.sla_target_hours,
    f.sla_breached,
    f.workload,
    f.cost,
    f.quality_score,
    c.customer_segment,
    c.customer_region,
    p.category,
    p.subcategory,
    e.department,
    e.experience_level,
    l.region,
    l.facility_type,
    l.capacity
FROM fact_operations f
LEFT JOIN dim_customer c ON f.customer_id = c.customer_id
LEFT JOIN dim_product p ON f.product_id = p.product_id
LEFT JOIN dim_employee e ON f.employee_id = e.employee_id
LEFT JOIN dim_location l ON f.location_id = l.location_id;


-- 2. Stage performance
CREATE OR REPLACE VIEW vw_stage_performance AS
SELECT
    stage_name,
    COUNT(*) AS operations,
    ROUND(AVG(stage_duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(target_time_minutes), 2) AS avg_target_minutes,
    ROUND(AVG(stage_variance_minutes), 2) AS avg_variance_minutes,
    ROUND(
        100.0 * AVG(
            CASE WHEN stage_status = 'Delayed' THEN 1 ELSE 0 END
        ),
        2
    ) AS delay_rate_pct
FROM fact_operation_stages
GROUP BY stage_name;


-- 3. Experience × workload RCA
CREATE OR REPLACE VIEW vw_experience_workload_rca AS
SELECT
    e.experience_level,
    CASE
        WHEN f.workload <= 5 THEN 'Low'
        WHEN f.workload <= 10 THEN 'Moderate'
        WHEN f.workload <= 15 THEN 'High'
        WHEN f.workload <= 20 THEN 'Very High'
        ELSE 'Extreme'
    END AS workload_band,
    COUNT(*) AS operations,
    ROUND(AVG(s.stage_duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(s.stage_variance_minutes), 2) AS avg_variance_minutes,
    ROUND(
        100.0 * AVG(
            CASE WHEN s.stage_status = 'Delayed' THEN 1 ELSE 0 END
        ),
        2
    ) AS delay_rate_pct
FROM fact_operation_stages s
JOIN fact_operations f
    ON s.operation_id = f.operation_id
JOIN dim_employee e
    ON f.employee_id = e.employee_id
WHERE s.stage_name = 'Quality Check'
GROUP BY
    e.experience_level,
    workload_band;