import os
import numpy as np
import pandas as pd
from faker import Faker

# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42
np.random.seed(SEED)

fake = Faker()
fake.seed_instance(SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)

# ============================================================
# PARAMETERS
# ============================================================

N_CUSTOMERS = 5_000
N_PRODUCTS = 500
N_EMPLOYEES = 500
N_LOCATIONS = 25
N_OPERATIONS = 150_000

START_DATE = "2021-01-01"
END_DATE = "2026-12-31"

# ============================================================
# DIMENSION: DATE
# ============================================================

def generate_date_dimension():

    dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="D"
    )

    df = pd.DataFrame({
        "date": dates
    })

    df["date_id"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["weekday"] = df["date"].dt.day_name()
    df["is_weekend"] = df["date"].dt.dayofweek >= 5

    # Indian public-holiday style dates for simulation
    holiday_dates = pd.to_datetime([
        "2021-01-26",
        "2021-08-15",
        "2021-10-02",
        "2022-01-26",
        "2022-08-15",
        "2022-10-02",
        "2023-01-26",
        "2023-08-15",
        "2023-10-02",
        "2024-01-26",
        "2024-08-15",
        "2024-10-02",
        "2025-01-26",
        "2025-08-15",
        "2025-10-02",
        "2026-01-26",
        "2026-08-15",
        "2026-10-02"
    ])

    df["is_holiday"] = df["date"].isin(holiday_dates)

    return df


# ============================================================
# DIMENSION: CUSTOMER
# ============================================================

def generate_customers():

    customer_ids = [
        f"CUST_{i:05d}"
        for i in range(1, N_CUSTOMERS + 1)
    ]

    segments = np.random.choice(
        ["Enterprise", "SMB", "Consumer"],
        size=N_CUSTOMERS,
        p=[0.20, 0.35, 0.45]
    )

    regions = np.random.choice(
        [
            "North",
            "South",
            "East",
            "West",
            "Central"
        ],
        size=N_CUSTOMERS
    )

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "customer_segment": segments,
        "region": regions
    })

    return df


# ============================================================
# DIMENSION: PRODUCT
# ============================================================

def generate_products():

    product_ids = [
        f"PROD_{i:04d}"
        for i in range(1, N_PRODUCTS + 1)
    ]

    categories = [
        "Electronics",
        "Home",
        "Industrial",
        "Healthcare",
        "Consumer Goods"
    ]

    category = np.random.choice(
        categories,
        size=N_PRODUCTS
    )

    subcategory_map = {
        "Electronics": ["Devices", "Accessories", "Components"],
        "Home": ["Furniture", "Appliances", "Decor"],
        "Industrial": ["Machinery", "Tools", "Equipment"],
        "Healthcare": ["Medical Devices", "Supplies", "Diagnostics"],
        "Consumer Goods": ["Personal Care", "Food", "Household"]
    }

    subcategories = [
        np.random.choice(subcategory_map[c])
        for c in category
    ]

    df = pd.DataFrame({
        "product_id": product_ids,
        "category": category,
        "subcategory": subcategories
    })

    return df


# ============================================================
# DIMENSION: EMPLOYEE
# ============================================================

def generate_employees():

    employee_ids = [
        f"EMP_{i:04d}"
        for i in range(1, N_EMPLOYEES + 1)
    ]

    departments = np.random.choice(
        [
            "Processing",
            "Quality",
            "Packaging",
            "Dispatch"
        ],
        size=N_EMPLOYEES,
        p=[0.40, 0.20, 0.20, 0.20]
    )

    teams = np.random.choice(
        [
            "Team A",
            "Team B",
            "Team C",
            "Team D",
            "Team E"
        ],
        size=N_EMPLOYEES
    )

    experience = np.random.choice(
        [
            "Junior",
            "Mid",
            "Senior"
        ],
        size=N_EMPLOYEES,
        p=[0.35, 0.45, 0.20]
    )

    df = pd.DataFrame({
        "employee_id": employee_ids,
        "department": departments,
        "team": teams,
        "experience_level": experience
    })

    return df


# ============================================================
# DIMENSION: LOCATION
# ============================================================

def generate_locations():

    location_ids = [
        f"LOC_{i:03d}"
        for i in range(1, N_LOCATIONS + 1)
    ]

    regions = np.random.choice(
        [
            "North",
            "South",
            "East",
            "West",
            "Central"
        ],
        size=N_LOCATIONS
    )

    facility_types = np.random.choice(
        [
            "Distribution Center",
            "Processing Hub",
            "Fulfillment Center"
        ],
        size=N_LOCATIONS
    )

    capacity = np.random.randint(
        350,
        1_001,
        size=N_LOCATIONS
    )

    df = pd.DataFrame({
        "location_id": location_ids,
        "region": regions,
        "facility_type": facility_types,
        "capacity": capacity
    })

    return df


# ============================================================
# FACT: OPERATIONS
# ============================================================

def generate_operations(
    customers,
    products,
    employees,
    locations,
    dates
):

    print("Generating operations...")

    operation_dates = pd.Series(
        np.random.choice(
            dates["date"].values,
            size=N_OPERATIONS
        )
    )

    operation_dates = pd.to_datetime(operation_dates)

    customer_ids = np.random.choice(
        customers["customer_id"],
        size=N_OPERATIONS
    )

    product_ids = np.random.choice(
        products["product_id"],
        size=N_OPERATIONS
    )

    employee_ids = np.random.choice(
        employees["employee_id"],
        size=N_OPERATIONS
    )

    location_ids = np.random.choice(
        locations["location_id"],
        size=N_OPERATIONS
    )

    # --------------------------------------------------------
    # Base demand
    # --------------------------------------------------------

    month = operation_dates.dt.month.values

    seasonal_factor = np.where(
        np.isin(month, [10, 11, 12]),
        1.30,
        1.00
    )

    weekday_factor = np.where(
        operation_dates.dt.dayofweek.values >= 5,
        0.70,
        1.00
    )

    demand_factor = (
        seasonal_factor *
        weekday_factor
    )

    quantity = np.maximum(
        1,
        np.random.poisson(
            8 * demand_factor
        )
    )

    # --------------------------------------------------------
    # Employee experience effect
    # --------------------------------------------------------

    employee_lookup = employees.set_index(
        "employee_id"
    )

    experience_values = employee_lookup.loc[
        employee_ids,
        "experience_level"
    ].values

    experience_factor = np.select(
        [
            experience_values == "Junior",
            experience_values == "Mid",
            experience_values == "Senior"
        ],
        [
            1.25,
            1.00,
            0.82
        ]
    )

    # --------------------------------------------------------
    # Processing time
    # --------------------------------------------------------

    base_processing = np.random.gamma(
        shape=3.0,
        scale=1.2,
        size=N_OPERATIONS
    )

    processing_time = (
        base_processing *
        experience_factor *
        demand_factor
    )

    # --------------------------------------------------------
    # Artificial bottleneck
    #
    # Quality operations intentionally take longer.
    # This creates something meaningful for our bottleneck
    # analysis later.
    # --------------------------------------------------------

    employee_department = employee_lookup.loc[
        employee_ids,
        "department"
    ].values

    quality_factor = np.where(
        employee_department == "Quality",
        2.0,
        1.0
    )

    processing_time *= quality_factor

    # --------------------------------------------------------
    # Workload
    # --------------------------------------------------------

    workload = np.clip(
        quantity * np.random.uniform(
            0.8,
            1.4,
            N_OPERATIONS
        ),
        1,
        None
    )

    # --------------------------------------------------------
    # Delay
    # --------------------------------------------------------

    delay_probability = np.clip(
        (
            0.03
            + (processing_time > 6) * 0.18
            + (workload > 15) * 0.12
            + (employee_department == "Quality") * 0.08
        ),
        0,
        0.85
    )

    delayed = (
        np.random.random(N_OPERATIONS)
        < delay_probability
    )

    delay_minutes = np.where(
        delayed,
        np.random.gamma(
            shape=2.0,
            scale=90,
            size=N_OPERATIONS
        ),
        0
    )

    delay_minutes = np.round(
        delay_minutes,
        2
    )

    # --------------------------------------------------------
    # SLA
    # --------------------------------------------------------

    sla_target_hours = np.where(
        employee_department == "Quality",
        8,
        6
    )

    total_time_hours = (
        processing_time +
        delay_minutes / 60
    )

    sla_breached = (
        total_time_hours >
        sla_target_hours
    )

    # --------------------------------------------------------
    # Quality score
    # --------------------------------------------------------

    quality_score = np.clip(
        96
        - processing_time * 1.2
        - delayed * 5
        + np.random.normal(
            0,
            3,
            N_OPERATIONS
        ),
        50,
        100
    )

    quality_score = np.round(
        quality_score,
        2
    )

    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    cost = (
        80
        + quantity * 5
        + processing_time * 25
        + delay_minutes * 0.75
    )

    cost += np.random.normal(
        0,
        15,
        N_OPERATIONS
    )

    cost = np.maximum(
        cost,
        20
    )

    cost = np.round(
        cost,
        2
    )

    # --------------------------------------------------------
    # Timestamps
    # --------------------------------------------------------

    start_time = (
        operation_dates
        + pd.to_timedelta(
            np.random.randint(
                7,
                19,
                N_OPERATIONS
            ),
            unit="h"
        )
        + pd.to_timedelta(
            np.random.randint(
                0,
                60,
                N_OPERATIONS
            ),
            unit="m"
        )
    )

    completion_time = (
        start_time
        + pd.to_timedelta(
            total_time_hours,
            unit="h"
        )
    )

    expected_completion = (
        start_time
        + pd.to_timedelta(
            sla_target_hours,
            unit="h"
        )
    )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    status = np.where(
        sla_breached,
        "Delayed",
        "Completed"
    )

    # --------------------------------------------------------
    # Create fact table
    # --------------------------------------------------------

    df = pd.DataFrame({

        "operation_id": [
            f"OP_{i:07d}"
            for i in range(1, N_OPERATIONS + 1)
        ],

        "order_id": [
            f"ORD_{i:07d}"
            for i in range(1, N_OPERATIONS + 1)
        ],

        "customer_id": customer_ids,

        "product_id": product_ids,

        "employee_id": employee_ids,

        "location_id": location_ids,

        "order_date": operation_dates,

        "start_time": start_time,

        "completion_time": completion_time,

        "expected_completion": expected_completion,

        "status": status,

        "quantity": quantity,

        "processing_time_hours": np.round(
            processing_time,
            2
        ),

        "delay_minutes": delay_minutes,

        "sla_target_hours": sla_target_hours,

        "sla_breached": sla_breached,

        "workload": np.round(
            workload,
            2
        ),

        "cost": cost,

        "quality_score": quality_score

    })

    return df


# ============================================================
# SAVE DATA
# ============================================================

def save_data(name, dataframe):

    path = os.path.join(
        RAW_DIR,
        f"{name}.csv"
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"{name}: {len(dataframe):,} rows → {path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n======================================")
    print("      OpsPulse Data Generator")
    print("======================================\n")

    print("Generating dimensions...")

    dates = generate_date_dimension()
    customers = generate_customers()
    products = generate_products()
    employees = generate_employees()
    locations = generate_locations()

    operations = generate_operations(
        customers,
        products,
        employees,
        locations,
        dates
    )

    print("\nSaving datasets...\n")

    save_data("dim_date", dates)
    save_data("dim_customer", customers)
    save_data("dim_product", products)
    save_data("dim_employee", employees)
    save_data("dim_location", locations)
    save_data("fact_operations", operations)

    print("\n======================================")
    print("       DATA GENERATION COMPLETE")
    print("======================================\n")


if __name__ == "__main__":
    main()