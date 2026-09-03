import os
import pandas as pd


# ============================================================
# PATH
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
# LOAD
# ============================================================

stage_path = os.path.join(
    RAW_DIR,
    "fact_operation_stages.csv"
)

operations_path = os.path.join(
    RAW_DIR,
    "fact_operations.csv"
)

stages = pd.read_csv(
    stage_path,
    parse_dates=[
        "stage_start_time",
        "stage_end_time"
    ]
)

operations = pd.read_csv(
    operations_path,
    parse_dates=[
        "start_time",
        "completion_time"
    ]
)


# ============================================================
# BASIC CHECKS
# ============================================================

print("=" * 60)
print("OpsPulse Stage Data Validation")
print("=" * 60)

print(
    f"\nStage records: "
    f"{len(stages):,}"
)

print(
    f"Unique operations: "
    f"{stages['operation_id'].nunique():,}"
)

print(
    f"Unique stages: "
    f"{stages['stage_name'].nunique()}"
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = stages.isnull().sum()

missing = missing[missing > 0]

if len(missing) == 0:
    print("✓ No missing values")
else:
    print(missing)


# ============================================================
# DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATES")
print("=" * 60)

duplicates = stages.duplicated(
    subset=[
        "operation_id",
        "stage_id"
    ]
).sum()

if duplicates == 0:
    print(
        "✓ No duplicate operation-stage combinations"
    )
else:
    print(
        f"⚠ {duplicates:,} duplicates found"
    )


# ============================================================
# STAGE COUNT PER OPERATION
# ============================================================

print("\n" + "=" * 60)
print("STAGE COUNT PER OPERATION")
print("=" * 60)

stage_counts = (
    stages
    .groupby("operation_id")
    .size()
)

invalid_counts = (
    stage_counts != 4
).sum()

if invalid_counts == 0:
    print(
        "✓ Every operation has exactly 4 stages"
    )
else:
    print(
        f"⚠ {invalid_counts:,} operations "
        f"do not have 4 stages"
    )


# ============================================================
# TIMESTAMP LOGIC
# ============================================================

print("\n" + "=" * 60)
print("TIMESTAMP VALIDATION")
print("=" * 60)

invalid_duration = (
    stages["stage_end_time"]
    <= stages["stage_start_time"]
).sum()

if invalid_duration == 0:
    print(
        "✓ All stage end times occur after start times"
    )
else:
    print(
        f"⚠ {invalid_duration:,} invalid timestamps"
    )


# ============================================================
# STAGE ORDER
# ============================================================

print("\n" + "=" * 60)
print("STAGE ORDER VALIDATION")
print("=" * 60)

expected_order = [
    "Processing",
    "Quality Check",
    "Packaging",
    "Dispatch"
]

invalid_order = 0

for operation_id, group in stages.groupby(
    "operation_id"
):

    actual_order = (
        group
        .sort_values("stage_sequence")
        ["stage_name"]
        .tolist()
    )

    if actual_order != expected_order:
        invalid_order += 1


if invalid_order == 0:
    print(
        "✓ Stage sequence is valid"
    )
else:
    print(
        f"⚠ {invalid_order:,} "
        f"operations have invalid stage order"
    )


# ============================================================
# REFERENTIAL INTEGRITY
# ============================================================

print("\n" + "=" * 60)
print("REFERENTIAL INTEGRITY")
print("=" * 60)

invalid_operations = (
    ~stages["operation_id"]
    .isin(operations["operation_id"])
).sum()

if invalid_operations == 0:
    print(
        "✓ All operation IDs exist in fact_operations"
    )
else:
    print(
        f"⚠ {invalid_operations:,} "
        f"invalid operation IDs"
    )


# ============================================================
# STAGE SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("STAGE SUMMARY")
print("=" * 60)

summary = (
    stages
    .groupby("stage_name")
    .agg(
        operations=("operation_id", "nunique"),
        avg_duration_minutes=(
            "stage_duration_minutes",
            "mean"
        ),
        target_minutes=(
            "target_time_minutes",
            "mean"
        ),
        avg_variance_minutes=(
            "stage_variance_minutes",
            "mean"
        ),
        delayed_pct=(
            "stage_status",
            lambda x:
            (x == "Delayed").mean() * 100
        )
    )
    .reset_index()
)

summary["variance_pct"] = (
    summary["avg_variance_minutes"]
    / summary["target_minutes"]
    * 100
)

print(
    summary.to_string(
        index=False
    )
)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("STAGE DATA VALIDATION COMPLETE")
print("=" * 60)