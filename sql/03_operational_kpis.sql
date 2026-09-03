-- ============================================================
-- OPERATIONAL KPI SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_operations,
    SUM(quantity) AS total_quantity,
    ROUND(AVG(processing_time_hours), 2) AS avg_processing_hours,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(AVG(quality_score), 2) AS avg_quality_score,
    ROUND(SUM(cost), 2) AS total_cost,
    ROUND(AVG(cost), 2) AS avg_cost_per_operation,
    ROUND(
        100.0 * AVG(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END),
        2
    ) AS sla_compliance_pct
FROM opspulse.fact_operations;

-- ============================================================
-- MONTHLY OPERATIONAL PERFORMANCE
-- ============================================================

SELECT
    DATE_TRUNC('month', order_date)::date AS month,
    COUNT(*) AS operations,
    SUM(quantity) AS quantity,
    ROUND(AVG(processing_time_hours), 2) AS avg_processing_hours,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * AVG(CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END),
        2
    ) AS sla_compliance_pct,
    ROUND(SUM(cost), 2) AS total_cost
FROM opspulse.fact_operations
GROUP BY 1
ORDER BY 1;

-- ============================================================
-- DEPARTMENT PERFORMANCE
-- ============================================================

SELECT
    e.department,
    COUNT(*) AS operations,
    ROUND(AVG(f.processing_time_hours), 2) AS avg_processing_hours,
    ROUND(AVG(f.delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * AVG(CASE WHEN f.sla_breached = FALSE THEN 1 ELSE 0 END),
        2
    ) AS sla_compliance_pct,
    ROUND(AVG(f.quality_score), 2) AS avg_quality_score,
    ROUND(SUM(f.cost), 2) AS total_cost
FROM opspulse.fact_operations f
JOIN opspulse.dim_employee e
    ON f.employee_id = e.employee_id
GROUP BY e.department
ORDER BY sla_compliance_pct ASC;

-- ============================================================
-- QUALITY CHECK BOTTLENECK
-- ============================================================

SELECT
    stage_name,
    COUNT(*) AS stage_operations,
    ROUND(AVG(stage_duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(target_time_minutes), 2) AS avg_target_minutes,
    ROUND(AVG(stage_variance_minutes), 2) AS avg_variance_minutes,
    ROUND(
        100.0 * AVG(
            CASE WHEN stage_status = 'Delayed' THEN 1 ELSE 0 END
        ),
        2
    ) AS delay_rate_pct
FROM opspulse.fact_operation_stages
GROUP BY stage_name
ORDER BY avg_variance_minutes DESC;

-- ============================================================
-- EMPLOYEE EXPERIENCE PERFORMANCE
-- ============================================================

SELECT
    e.experience_level,
    COUNT(*) AS operations,
    ROUND(AVG(f.processing_time_hours), 2) AS avg_processing_hours,
    ROUND(AVG(f.delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * AVG(
            CASE WHEN f.sla_breached = FALSE THEN 1 ELSE 0 END
        ),
        2
    ) AS sla_compliance_pct,
    ROUND(AVG(f.quality_score), 2) AS avg_quality_score
FROM opspulse.fact_operations f
JOIN opspulse.dim_employee e
    ON f.employee_id = e.employee_id
GROUP BY e.experience_level
ORDER BY sla_compliance_pct ASC;

-- ============================================================
-- WORKLOAD PERFORMANCE
-- ============================================================

SELECT
    workload_band,
    COUNT(*) AS operations,
    ROUND(AVG(processing_time_hours), 2) AS avg_processing_hours,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * AVG(
            CASE WHEN sla_breached = FALSE THEN 1 ELSE 0 END
        ),
        2
    ) AS sla_compliance_pct,
    ROUND(AVG(quality_score), 2) AS avg_quality_score
FROM (
    SELECT
        *,
        CASE
            WHEN workload <= 5 THEN 'Low'
            WHEN workload <= 10 THEN 'Moderate'
            WHEN workload <= 15 THEN 'High'
            WHEN workload <= 20 THEN 'Very High'
            ELSE 'Extreme'
        END AS workload_band
    FROM opspulse.fact_operations
) f
GROUP BY workload_band
ORDER BY
    CASE workload_band
        WHEN 'Low' THEN 1
        WHEN 'Moderate' THEN 2
        WHEN 'High' THEN 3
        WHEN 'Very High' THEN 4
        WHEN 'Extreme' THEN 5
    END;

-- ============================================================
-- QUALITY CHECK RCA — EXPERIENCE × WORKLOAD
-- ============================================================

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
FROM opspulse.fact_operation_stages s
JOIN opspulse.fact_operations f
    ON s.operation_id = f.operation_id
JOIN opspulse.dim_employee e
    ON f.employee_id = e.employee_id
WHERE s.stage_name = 'Quality Check'
GROUP BY
    e.experience_level,
    workload_band
ORDER BY
    e.experience_level,
    delay_rate_pct DESC;