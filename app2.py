import streamlit as st
import pandas as pd
import plotly.express as px

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(
    page_title="Complaint Dashboard",
    layout="wide"
)

st.title("Complaint Management Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("ComplaintsData.xlsx")

    if "LogedDate" in df.columns:
        df["LogedDate"] = pd.to_datetime(
            df["LogedDate"],
            errors="coerce"
        )

    if "resolveDate" in df.columns:
        df["resolveDate"] = pd.to_datetime(
            df["resolveDate"],
            errors="coerce"
        )

    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

search = st.sidebar.text_input("Search")

status = st.sidebar.multiselect(
    "Status",
    sorted(df["Status"].dropna().unique())
)

company = st.sidebar.multiselect(
    "Company",
    sorted(df["Company_Name"].dropna().unique())
)

plant = st.sidebar.multiselect(
    "Plant",
    sorted(df["plantname"].dropna().unique())
)

problem = st.sidebar.multiselect(
    "Problem",
    sorted(df["Problem_Name"].dropna().unique())
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if search:
    mask = filtered_df.astype(str).apply(
        lambda col: col.str.contains(
            search,
            case=False,
            na=False
        )
    ).any(axis=1)

    filtered_df = filtered_df[mask]

if status:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(status)
    ]

if company:
    filtered_df = filtered_df[
        filtered_df["Company_Name"].isin(company)
    ]

if plant:
    filtered_df = filtered_df[
        filtered_df["plantname"].isin(plant)
    ]

if problem:
    filtered_df = filtered_df[
        filtered_df["Problem_Name"].isin(problem)
    ]

# -----------------------------
# KPI Cards
# -----------------------------
total = len(filtered_df)

resolved = len(
    filtered_df[
        filtered_df["Status"]
        .astype(str)
        .str.lower()
        .str.contains("resolved")
    ]
)

open_count = total - resolved

avg_hours = (
    filtered_df["ResolutionInHrs"]
    .fillna(0)
    .mean()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Complaints", total)
c2.metric("Open", open_count)
c3.metric("Resolved", resolved)
c4.metric("Avg Resolution Hrs",
          round(avg_hours, 2))

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    status_chart = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_chart.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_chart,
        values="Count",
        names="Status",
        title="Complaint Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    problem_chart = (
        filtered_df["Problem_Name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    problem_chart.columns = [
        "Problem",
        "Count"
    ]

    fig = px.bar(
        problem_chart,
        x="Count",
        y="Problem",
        orientation="h",
        title="Top Complaint Types"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Monthly Trend
# -----------------------------
if "LogedDate" in filtered_df.columns:

    trend = filtered_df.copy()

    trend["Month"] = (
        trend["LogedDate"]
        .dt.to_period("M")
        .astype(str)
    )

    trend = (
        trend.groupby("Month")
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        trend,
        x="Month",
        y="Count",
        markers=True,
        title="Monthly Complaint Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Export
# -----------------------------
csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    "Download Filtered Data",
    csv,
    "complaints.csv",
    "text/csv"
)

# -----------------------------
# Data Grid
# -----------------------------
st.subheader("Complaint Records")

gb = GridOptionsBuilder.from_dataframe(
    filtered_df
)

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True
)

gb.configure_pagination(
    paginationPageSize=25
)

grid_options = gb.build()

AgGrid(
    filtered_df,
    gridOptions=grid_options,
    height=600
)