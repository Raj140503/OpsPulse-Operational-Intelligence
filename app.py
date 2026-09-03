import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="OpsPulse – Operational Intelligence",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data" / "processed"


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("OpsPulse – Operational Intelligence Platform")
st.caption(
    "Operations, Bottleneck, Workforce, Quality & Cost Intelligence"
)


# ---------------------------------------------------------
# Load Processed Datasets
# ---------------------------------------------------------

csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    st.error("No processed CSV files found.")
    st.stop()

datasets = {}

for file in csv_files:
    try:
        datasets[file.stem] = pd.read_csv(file)
    except Exception as e:
        st.warning(f"Could not load {file.name}: {e}")


st.success(
    f"{len(datasets)} processed datasets loaded successfully."
)


# ---------------------------------------------------------
# Executive KPIs
# ---------------------------------------------------------

if "executive_kpis" in datasets:

    kpis = datasets["executive_kpis"].iloc[0]

    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Operations",
        f"{kpis['Total Operations']:,.0f}"
    )

    col2.metric(
        "SLA Compliance",
        f"{kpis['SLA Compliance %']:.1f}%"
    )

    col3.metric(
        "Avg Processing Time",
        f"{kpis['Average Processing Hours']:.2f} hrs"
    )

    col4.metric(
        "Avg Delay",
        f"{kpis['Average Delay Minutes']:.2f} min"
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Total Cost",
        f"{kpis['Total Cost']:,.0f}"
    )

    col6.metric(
        "Avg Quality Score",
        f"{kpis['Average Quality Score']:.2f}"
    )

    col7.metric(
        "Total Quantity",
        f"{kpis['Total Quantity']:,.0f}"
    )

    col8.metric(
        "Cost / Operation",
        f"{kpis['Cost per Operation']:.2f}"
    )


# ---------------------------------------------------------
# Dataset Overview
# ---------------------------------------------------------

st.subheader("Available Analytical Datasets")

dataset_info = pd.DataFrame([
    {
        "Dataset": name,
        "Rows": df.shape[0],
        "Columns": df.shape[1]
    }
    for name, df in datasets.items()
])

st.dataframe(
    dataset_info,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# Operational Bottlenecks
# ---------------------------------------------------------

if "stage_performance" in datasets:

    stage = datasets["stage_performance"].copy()

    # Convert numeric columns
    stage["avg_duration_minutes"] = pd.to_numeric(
        stage["avg_duration_minutes"],
        errors="coerce"
    )

    stage["target_time_minutes"] = pd.to_numeric(
        stage["target_time_minutes"],
        errors="coerce"
    )

    st.subheader("Operational Bottlenecks")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=stage["stage_name"],
            y=stage["avg_duration_minutes"],
            name="Average Duration"
        )
    )

    fig.add_trace(
        go.Bar(
            x=stage["stage_name"],
            y=stage["target_time_minutes"],
            name="Target Duration"
        )
    )

    fig.update_layout(
        title="Stage Duration vs Target",
        xaxis_title="Stage",
        yaxis_title="Duration (Minutes)",
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# Stage Delay Rate
# ---------------------------------------------------------

if "stage_performance" in datasets:

    st.subheader("Stage Delay Rate")

    stage_delay = datasets["stage_performance"].copy()

    stage_delay["operations"] = pd.to_numeric(
        stage_delay["operations"],
        errors="coerce"
    )

    stage_delay["delayed_operations"] = pd.to_numeric(
        stage_delay["delayed_operations"],
        errors="coerce"
    )

    # Calculate delay rate directly
    stage_delay["delay_rate"] = (
        stage_delay["delayed_operations"]
        / stage_delay["operations"]
        * 100
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=stage_delay["stage_name"].tolist(),
            y=stage_delay["delay_rate"].tolist(),
            name="Delay Rate",
            text=[
                f"{value:.1f}%"
                for value in stage_delay["delay_rate"]
            ],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Delay Rate by Operational Stage",
        xaxis_title="Stage",
        yaxis_title="Delay Rate (%)",
        yaxis=dict(
            range=[0, 70],
            dtick=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# Experience × Workload RCA
# ---------------------------------------------------------

if "quality_experience_workload_rca" in datasets:

    st.subheader("Experience × Workload RCA")

    rca = datasets["quality_experience_workload_rca"].copy()

    rca["delay_rate_pct"] = pd.to_numeric(
        rca["delay_rate_pct"],
        errors="coerce"
    )

    # Convert decimal rates to percentages if necessary
    if rca["delay_rate_pct"].max() <= 1:
        rca["delay_rate_pct"] = rca["delay_rate_pct"] * 100

    fig = go.Figure()

    for experience_level in rca["experience_level"].dropna().unique():

        subset = rca[
            rca["experience_level"] == experience_level
        ]

        fig.add_trace(
            go.Bar(
                x=subset["workload_band"].tolist(),
                y=subset["delay_rate_pct"].tolist(),
                name=experience_level,
                text=[
                    f"{value:.1f}%"
                    for value in subset["delay_rate_pct"]
                ],
                textposition="outside"
            )
        )

    fig.update_layout(
        title="Delay Rate by Experience and Workload",
        xaxis_title="Workload Level",
        yaxis_title="Delay Rate (%)",
        barmode="group",
        yaxis=dict(
            range=[0, 90],
            dtick=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if "bottleneck_workload_analysis" in datasets:

    workload = datasets["bottleneck_workload_analysis"]

    st.subheader("Workload Performance")


    st.dataframe(
        workload,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# Workload Performance
# ---------------------------------------------------------

if "bottleneck_workload_analysis" in datasets:

    st.subheader("Workload Performance")

    workload = datasets["bottleneck_workload_analysis"].copy()

    # Convert to numeric
    operations = pd.to_numeric(
        workload["operations"],
        errors="coerce"
    )

    delay_rate = pd.to_numeric(
        workload["delay_rate_pct"],
        errors="coerce"
    )

    # Values are already percentages
    delay_values = delay_rate.astype(float).tolist()

    workload_labels = workload[
        "workload_band"
    ].astype(str).tolist()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=workload_labels,
            y=delay_values,
            name="Delay Rate",
            text=[
                f"{value:.1f}%"
                for value in delay_values
            ],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="Quality Check Delay Rate by Workload",
        xaxis_title="Workload Level",
        yaxis_title="Delay Rate (%)",
        barmode="group",
        yaxis=dict(
            range=[0, 85],
            dtick=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if "quality_rca_correlation" in datasets:

    quality_cost = datasets["quality_rca_correlation"]

    st.subheader("Quality vs Cost Analysis")


    st.dataframe(
        quality_cost,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# Quality RCA
# ---------------------------------------------------------

if "quality_experience_rca" in datasets:

    quality_rca = datasets["quality_experience_rca"]

    st.subheader("Quality RCA")


    st.dataframe(
        quality_rca,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# Quality RCA - Experience Column Chart
# ---------------------------------------------------------

if "quality_experience_rca" in datasets:

    st.subheader("Delay Rate by Employee Experience")

    quality_rca = datasets["quality_experience_rca"].copy()

    # Convert to numeric
    quality_rca["delay_rate_pct"] = pd.to_numeric(
        quality_rca["delay_rate_pct"],
        errors="coerce"
    )

    # Your dataset stores values such as 69.0663 = 69.0663%
    # If values are stored as decimals such as 0.690663, convert them.
    if quality_rca["delay_rate_pct"].max() <= 1:
        quality_rca["delay_rate_pct"] = (
            quality_rca["delay_rate_pct"] * 100
        )

    # Create explicit text labels
    quality_rca["label"] = quality_rca["delay_rate_pct"].apply(
        lambda x: f"{x:.1f}%"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=quality_rca["experience_level"].tolist(),
            y=quality_rca["delay_rate_pct"].tolist(),
            text=quality_rca["label"].tolist(),
            textposition="outside",
            name="Delay Rate"
        )
    )

    fig.update_layout(
        title="Quality Check Delay Rate by Employee Experience",
        xaxis_title="Experience Level",
        yaxis_title="Delay Rate (%)",
        yaxis=dict(
            range=[0, 80],
            dtick=10
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# RCA Priority - Inspect Dataset
# ---------------------------------------------------------

if "quality_rca_priority" in datasets:

    st.subheader("RCA Priority Analysis")

    priority = datasets["quality_rca_priority"].copy()


    st.dataframe(
        priority,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# RCA Priority Analysis
# ---------------------------------------------------------

if "quality_rca_priority" in datasets:

    priority = datasets["quality_rca_priority"].copy()

    priority_levels = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Very High": 4
    }

    # Clean text values
    priority["factor"] = priority["factor"].astype(str).str.strip()
    priority["priority"] = priority["priority"].astype(str).str.strip()

    # Explicitly create numeric priority
    priority["priority_score"] = priority["priority"].apply(
        lambda x: priority_levels.get(x, 0)
    )

    st.subheader("RCA Priority Analysis")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=priority["factor"].tolist(),
            y=priority["priority_score"].tolist(),
            text=priority["priority"].tolist(),
            textposition="outside",
            name="Priority"
        )
    )

    fig.update_layout(
        title="Operational RCA Priority",
        xaxis_title="RCA Factor",
        yaxis_title="Priority Level",
        showlegend=False,
        yaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3, 4],
            ticktext=["Low", "Medium", "High", "Very High"],
            range=[0, 4.5]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# Management Recommendations
# ---------------------------------------------------------

st.subheader("Management Recommendations")

recommendations = [
    "Optimize the Quality Check stage — it has the highest delay rate at 59.0%.",
    "Reduce workload pressure during Very High and Extreme workload periods.",
    "Provide additional training and support for Junior employees.",
    "Prioritize Junior employees handling Extreme workload — delay rate reaches 83.8%.",
    "Balance operational speed with quality and cost performance."
]

for i, recommendation in enumerate(recommendations, 1):
    st.markdown(f"**{i}.** {recommendation}")