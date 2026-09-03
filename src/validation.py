import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    data = {}

    files = [
        "dim_date",
        "dim_customer",
        "dim_product",
        "dim_employee",
        "dim_location",
        "fact_operations"
    ]

    for file in files:

        path = os.path.join(
            RAW_DIR,
            f"{file}.csv"
        )

        data[file] = pd.read_csv(path)

        print(
            f"Loaded {file}: "
            f"{len(data[file]):,} rows"
        )

    return data


# ============================================================
# BASIC QUALITY CHECKS
# ============================================================

def check_missing_values(data):

    print("\n" + "=" * 60)
    print("MISSING VALUE CHECK")
    print("=" * 60)

    for name, df in data.items():

        missing = df.isnull().sum()

        missing = missing[
            missing > 0
        ]

        if len(missing) == 0:

            print(
                f"✓ {name}: No missing values"
            )

        else:

            print(
                f"⚠ {name}: Missing values found"
            )

            print(missing)


# ============================================================
# DUPLICATE CHECK
# ============================================================

def check_duplicates(data):

    print("\n" + "=" * 60)
    print("DUPLICATE CHECK")
    print("=" * 60)

    for name, df in data.items():

        duplicates = df.duplicated().sum()

        if duplicates == 0:

            print(
                f"✓ {name}: No duplicate rows"
            )

        else:

            print(
                f"⚠ {name}: "
                f"{duplicates:,} duplicate rows"
            )


# ============================================================
# PRIMARY KEY CHECK
# ============================================================

def check_primary_keys(data):

    print("\n" + "=" * 60)
    print("PRIMARY KEY CHECK")
    print("=" * 60)

    primary_keys = {

        "dim_date": "date_id",

        "dim_customer": "customer_id",

        "dim_product": "product_id",

        "dim_employee": "employee_id",

        "dim_location": "location_id",

        "fact_operations": "operation_id"
    }

    for table, key in primary_keys.items():

        df = data[table]

        duplicate_keys = df[key].duplicated().sum()

        null_keys = df[key].isnull().sum()

        if (
            duplicate_keys == 0
            and null_keys == 0
        ):

            print(
                f"✓ {table}.{key}: Valid"
            )

        else:

            print(
                f"⚠ {table}.{key}: "
                f"{duplicate_keys} duplicates, "
                f"{null_keys} nulls"
            )


# ============================================================
# FOREIGN KEY CHECK
# ============================================================

def check_foreign_keys(data):

    print("\n" + "=" * 60)
    print("FOREIGN KEY CHECK")
    print("=" * 60)

    fact = data["fact_operations"]

    relationships = {

        "customer_id":
            data["dim_customer"]["customer_id"],

        "product_id":
            data["dim_product"]["product_id"],

        "employee_id":
            data["dim_employee"]["employee_id"],

        "location_id":
            data["dim_location"]["location_id"]
    }

    for column, valid_values in relationships.items():

        invalid = (
            ~fact[column].isin(
                valid_values
            )
        ).sum()

        if invalid == 0:

            print(
                f"✓ fact_operations.{column}: Valid"
            )

        else:

            print(
                f"⚠ fact_operations.{column}: "
                f"{invalid:,} invalid keys"
            )


# ============================================================
# NUMERIC VALIDATION
# ============================================================

def check_numeric_ranges(data):

    print("\n" + "=" * 60)
    print("NUMERIC RANGE CHECK")
    print("=" * 60)

    fact = data["fact_operations"]

    checks = {

        "quantity":
            (fact["quantity"] >= 1).all(),

        "processing_time_hours":
            (fact["processing_time_hours"] > 0).all(),

        "delay_minutes":
            (fact["delay_minutes"] >= 0).all(),

        "cost":
            (fact["cost"] > 0).all(),

        "quality_score":
            (
                (fact["quality_score"] >= 0)
                &
                (fact["quality_score"] <= 100)
            ).all(),

        "sla_target_hours":
            (fact["sla_target_hours"] > 0).all(),

        "workload":
            (fact["workload"] > 0).all()
    }

    for column, valid in checks.items():

        if valid:

            print(
                f"✓ {column}: Valid"
            )

        else:

            print(
                f"⚠ {column}: Invalid values found"
            )


# ============================================================
# DATE VALIDATION
# ============================================================

def check_dates(data):

    print("\n" + "=" * 60)
    print("DATE VALIDATION")
    print("=" * 60)

    fact = data["fact_operations"].copy()

    fact["order_date"] = pd.to_datetime(
        fact["order_date"],
        errors="coerce"
    )

    fact["start_time"] = pd.to_datetime(
        fact["start_time"],
        errors="coerce"
    )

    fact["completion_time"] = pd.to_datetime(
        fact["completion_time"],
        errors="coerce"
    )

    fact["expected_completion"] = pd.to_datetime(
        fact["expected_completion"],
        errors="coerce"
    )

    invalid_order_dates = fact["order_date"].isnull().sum()

    invalid_start_dates = fact["start_time"].isnull().sum()

    invalid_completion_dates = (
        fact["completion_time"].isnull().sum()
    )

    invalid_expected_dates = (
        fact["expected_completion"].isnull().sum()
    )

    if (
        invalid_order_dates
        + invalid_start_dates
        + invalid_completion_dates
        + invalid_expected_dates
        == 0
    ):

        print("✓ All operational dates are valid")

    else:

        print("⚠ Invalid dates detected")


# ============================================================
# TIMESTAMP LOGIC
# ============================================================

def check_timestamp_logic(data):

    print("\n" + "=" * 60)
    print("TIMESTAMP LOGIC CHECK")
    print("=" * 60)

    fact = data["fact_operations"].copy()

    fact["start_time"] = pd.to_datetime(
        fact["start_time"]
    )

    fact["completion_time"] = pd.to_datetime(
        fact["completion_time"]
    )

    fact["expected_completion"] = pd.to_datetime(
        fact["expected_completion"]
    )

    invalid_completion = (
        fact["completion_time"]
        < fact["start_time"]
    ).sum()

    invalid_expected = (
        fact["expected_completion"]
        < fact["start_time"]
    ).sum()

    if invalid_completion == 0:

        print(
            "✓ Completion time occurs after start time"
        )

    else:

        print(
            f"⚠ {invalid_completion:,} "
            f"invalid completion timestamps"
        )

    if invalid_expected == 0:

        print(
            "✓ Expected completion time is valid"
        )

    else:

        print(
            f"⚠ {invalid_expected:,} "
            f"invalid expected completion timestamps"
        )


# ============================================================
# SLA LOGIC
# ============================================================

def check_sla_logic(data):

    print("\n" + "=" * 60)
    print("SLA LOGIC CHECK")
    print("=" * 60)

    fact = data["fact_operations"].copy()

    fact["start_time"] = pd.to_datetime(
        fact["start_time"]
    )

    fact["completion_time"] = pd.to_datetime(
        fact["completion_time"]
    )

    calculated_hours = (
        fact["completion_time"]
        - fact["start_time"]
    ).dt.total_seconds() / 3600

    calculated_breach = (
        calculated_hours
        > fact["sla_target_hours"]
    )

    mismatch = (
        calculated_breach
        != fact["sla_breached"]
    ).sum()

    if mismatch == 0:

        print(
            "✓ SLA breach logic is consistent"
        )

    else:

        print(
            f"⚠ {mismatch:,} SLA records "
            f"have inconsistent breach flags"
        )


# ============================================================
# DATASET SUMMARY
# ============================================================

def generate_summary(data):

    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    for name, df in data.items():

        print(
            f"{name:<25}"
            f"{len(df):>10,} rows"
            f"{len(df.columns):>10} columns"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("        OpsPulse Data Quality Pipeline")
    print("=" * 60)

    data = load_data()

    check_missing_values(data)

    check_duplicates(data)

    check_primary_keys(data)

    check_foreign_keys(data)

    check_numeric_ranges(data)

    check_dates(data)

    check_timestamp_logic(data)

    check_sla_logic(data)

    generate_summary(data)

    print("\n")
    print("=" * 60)
    print("        DATA QUALITY CHECK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()