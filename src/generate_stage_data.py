import os
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42
np.random.seed(SEED)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)

os.makedirs(RAW_DIR, exist_ok=True)


# ============================================================
# LOAD OPERATIONS
# ============================================================

operations_path = os.path.join(
    RAW_DIR,
    "fact_operations.csv"
)

operations = pd.read_csv(
    operations_path,
    parse_dates=[
        "order_date",
        "start_time",
        "completion_time",
        "expected_completion"
    ]
)

print(
    f"Loaded operations: {len(operations):,}"
)


# ============================================================
# STAGE CONFIGURATION
# ============================================================

stages = [
    {
        "stage_id": "STG_01",
        "stage_name": "Processing",
        "base_share": 0.30,
        "target_time_minutes": 90
    },
    {
        "stage_id": "STG_02",
        "stage_name": "Quality Check",
        "base_share": 0.40,
        "target_time_minutes": 75
    },
    {
        "stage_id": "STG_03",
        "stage_name": "Packaging",
        "base_share": 0.18,
        "target_time_minutes": 45
    },
    {
        "stage_id": "STG_04",
        "stage_name": "Dispatch",
        "base_share": 0.12,
        "target_time_minutes": 40
    }
]


# ============================================================
# GENERATE STAGE RECORDS
# ============================================================

stage_records = []

print("Generating stage-level records...")


for _, operation in operations.iterrows():

    operation_id = operation["operation_id"]

    start_time = operation["start_time"]

    total_processing_minutes = (
        operation["processing_time_hours"] * 60
    )

    workload = operation["workload"]

    # --------------------------------------------------------
    # Workload pressure
    # --------------------------------------------------------

    workload_factor = np.clip(
        1 + max(workload - 10, 0) * 0.025,
        1,
        1.60
    )

    # --------------------------------------------------------
    # Stage durations
    #
    # Quality is intentionally more sensitive to workload.
    # This creates a realistic bottleneck pattern.
    # --------------------------------------------------------

    raw_shares = np.array([
        0.30,
        0.40 * workload_factor,
        0.18,
        0.12
    ])

    raw_shares = (
        raw_shares /
        raw_shares.sum()
    )

    durations = (
        raw_shares *
        total_processing_minutes
    )

    # Add small operational variation
    variation = np.random.normal(
        1.0,
        0.08,
        4
    )

    durations *= variation

    durations = np.maximum(
        durations,
        1
    )

    # --------------------------------------------------------
    # Normalize so stage durations equal total processing time
    # --------------------------------------------------------

    durations *= (
        total_processing_minutes /
        durations.sum()
    )

    # --------------------------------------------------------
    # Generate sequential timestamps
    # --------------------------------------------------------

    current_start = start_time

    for i, stage in enumerate(stages):

        duration_minutes = durations[i]

        stage_start = current_start

        stage_end = (
            stage_start
            + pd.to_timedelta(
                duration_minutes,
                unit="m"
            )
        )

        target_minutes = (
            stage["target_time_minutes"]
        )

        stage_status = (
            "Delayed"
            if duration_minutes > target_minutes
            else "Within Target"
        )

        stage_records.append({

            "operation_id": operation_id,

            "stage_id": stage["stage_id"],

            "stage_name": stage["stage_name"],

            "stage_sequence": i + 1,

            "stage_start_time": stage_start,

            "stage_end_time": stage_end,

            "stage_duration_minutes": round(
                duration_minutes,
                2
            ),

            "target_time_minutes": (
                target_minutes
            ),

            "stage_variance_minutes": round(
                duration_minutes - target_minutes,
                2
            ),

            "stage_status": stage_status
        })

        current_start = stage_end


# ============================================================
# CREATE DATAFRAME
# ============================================================

stage_df = pd.DataFrame(
    stage_records
)


# ============================================================
# SORT
# ============================================================

stage_df = stage_df.sort_values(
    [
        "operation_id",
        "stage_sequence"
    ]
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

output_path = os.path.join(
    RAW_DIR,
    "fact_operation_stages.csv"
)

stage_df.to_csv(
    output_path,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n==============================================")
print("     STAGE DATA GENERATION COMPLETE")
print("==============================================")

print(
    f"Operations:      {operations['operation_id'].nunique():,}"
)

print(
    f"Stage records:   {len(stage_df):,}"
)

print(
    f"Unique stages:   {stage_df['stage_name'].nunique()}"
)

print(
    f"Output:          {output_path}"
)

print("\nStage distribution:")

print(
    stage_df["stage_name"]
    .value_counts()
)

print("\nSample records:")

print(
    stage_df.head(8).to_string(
        index=False
    )
)