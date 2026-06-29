# ==========================
# ✅ IMPORTS
# ==========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================
# ✅ SIMULATION ENGINE
# ==========================
process_steps = {
    "BRD Retrieval": (10, 5),
    "aLex Entry": (20, 10),
    "Document Upload": (8, 3),
    "AI Processing": (2, 1),
    "CCD Product Validation": (25, 10),
    "CCD Scope Validation": (15, 5),
    "Quality Check": (10, 4),
    "Publishing": (5, 2)
}

def simulate_contract():
    step_times = {}

    for step, (mean, std) in process_steps.items():
        time_taken = max(0, np.random.normal(mean, std))

        # Delay logic
        if step == "BRD Retrieval" and np.random.rand() < 0.2:
            time_taken += 15

        # Rework logic
        if step == "CCD Product Validation" and np.random.rand() < 0.15:
            time_taken *= 1.5

        step_times[step] = round(time_taken, 2)

    step_times["Total Time"] = round(sum(step_times.values()), 2)
    return step_times

def run_simulation(n=100):
    return [simulate_contract() for _ in range(n)]

# ==========================
# ✅ ANALYSIS
# ==========================
def analyze_results(data):
    df = pd.DataFrame(data)

    summary = {
        "Average Time": df["Total Time"].mean(),
        "Min Time": df["Total Time"].min(),
        "Max Time": df["Total Time"].max(),
    }

    step_avg = (
        df.mean(numeric_only=True)
        .drop("Total Time")
        .sort_values(ascending=False)
    )

    return df, summary, step_avg

# ==========================
# ✅ VISUALS
# ==========================
def plot_distribution(df):
    fig, ax = plt.subplots()

    sns.histplot(df["Total Time"], bins=20, kde=True, ax=ax)

    ax.set_title("Contract Processing Time Distribution")
    ax.set_xlabel("Time (mins)")
    ax.set_ylabel("Frequency")

    return fig


def plot_bottlenecks(step_avg):
    fig, ax = plt.subplots()  # ✅ FIX applied

    step_avg.plot(kind='bar', ax=ax, color='skyblue')

    ax.set_title("Average Time per Step")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Process Steps")
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    return fig

# ==========================
# ✅ STREAMLIT DASHBOARD
# ==========================
st.set_page_config(page_title="CCD DILO Dashboard", layout="wide")

st.title("📊 CCD MCI – DILO Analytics Dashboard")

# Input
num_contracts = st.slider("Select number of contracts", 50, 500, 200)

# Run model
data = run_simulation(num_contracts)
df, summary, step_avg = analyze_results(data)

# ==========================
# ✅ KPIs
# ==========================
col1, col2, col3 = st.columns(3)

col1.metric("Avg Time (mins)", round(summary["Average Time"], 2))
col2.metric("Min Time (mins)", round(summary["Min Time"], 2))
col3.metric("Max Time (mins)", round(summary["Max Time"], 2))

# Productivity
work_minutes = 480
contracts_per_day = work_minutes / summary["Average Time"]

st.success(f"✅ Contracts per Day: {round(contracts_per_day, 2)}")

# ==========================
# ✅ DATA TABLE
# ==========================
st.subheader("📋 Simulation Data")
st.dataframe(df.head(20))

# ==========================
# ✅ CHARTS
# ==========================
st.subheader("📊 Time Distribution")
st.pyplot(plot_distribution(df))

st.subheader("🔥 Bottleneck Analysis")
st.pyplot(plot_bottlenecks(step_avg))

# ==========================
# ✅ INSIGHTS
# ==========================
st.subheader("💡 Key Insights")

top_bottleneck = step_avg.index[0]

st.write(f"""
- Primary Bottleneck: **{top_bottleneck}**
- Avg Cycle Time: **{round(summary['Average Time'], 2)} mins**
- Throughput: **{round(contracts_per_day, 2)} contracts/day**

**Key Drivers:**
- BRD access delay
- Validation rework (CCD Product Validation)
""")
