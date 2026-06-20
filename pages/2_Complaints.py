import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from auth import is_authenticated,logout

# =====================================================
# AUTH CHECK
# =====================================================

if not is_authenticated():

    st.warning(
        "Session expired. Please login again."
    )

    st.switch_page("app3.py")

# =====================================================
# DATA CHECK
# =====================================================

if "df" not in st.session_state:

    st.warning(
        "Please upload an Excel file first."
    )

    st.stop()

df = st.session_state["df"]

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #1e293b 100%
        );

    color: white;
}

/* =====================================================
TITLE
===================================================== */

.page-title {

    font-size: 38px;

    font-weight: 700;

    color: white;

    margin-bottom: 5px;
}

.page-subtitle {

    color: #94a3b8;

    margin-bottom: 30px;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {

    background:
        rgba(15,23,42,0.95);
}

/* =====================================================
FILTER BOX
===================================================== */

[data-testid="stMultiSelect"] {

    background:
        rgba(255,255,255,0.04);

    border-radius: 12px;
}

/* =====================================================
CARD
===================================================== */

.metric-card {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 20px;

    padding: 25px;

    transition: 0.3s;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.25);
}

.metric-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 12px 40px rgba(0,0,0,0.35);
}

/* =====================================================
METRIC VALUE
===================================================== */

.metric-value {

    font-size: 36px;

    font-weight: 700;

    color: white;
}

/* =====================================================
METRIC LABEL
===================================================== */

.metric-label {

    color: #94a3b8;

    margin-top: 8px;

    font-size: 15px;
}

/* =====================================================
SECTION CARD
===================================================== */

.section-card {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 20px;

    padding: 25px;

    margin-top: 25px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.25);
}

/* =====================================================
DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border:
        1px solid rgba(255,255,255,0.08);
}

/* =====================================================
HEADINGS
===================================================== */

h3 {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="page-title">
📊 Complaint Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-subtitle">

Monitor complaint performance,
resolution efficiency, and root cause trends.

</div>
""", unsafe_allow_html=True)

# =====================================================
#AUTO REFRESH
# =====================================================

st_autorefresh(
    interval=1000,
    key="refresh"
)


# =====================================================
#SESSION TIMER
# =====================================================

remaining = (
    st.session_state["expiry"]
    - datetime.now()
)

remaining_seconds = max(
    0,
    int(remaining.total_seconds())
)

minutes = remaining_seconds // 60
seconds = remaining_seconds % 60

if remaining_seconds <= 0:

    logout()

    st.rerun()
    
st.sidebar.success(
    f"👋 {st.session_state['username']}"
)

st.sidebar.info(
    f"""
⏳ Session Timeout

{minutes:02}:{seconds:02}
"""
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown("## 🎯 Filters")

company = st.sidebar.multiselect(
    "Company",
    sorted(
        df["Company_Name"]
        .dropna()
        .unique()
    )
)

status = st.sidebar.multiselect(
    "Status",
    sorted(
        df["Status"]
        .dropna()
        .unique()
    )
)

plant = st.sidebar.multiselect(
    "Plant",
    sorted(
        df["plantname"]
        .dropna()
        .unique()
    )
)

problem = st.sidebar.multiselect(
    "Problem",
    sorted(
        df["Problem_Name"]
        .dropna()
        .unique()
    )
)

# =====================================================
# FILTERING
# =====================================================

filtered = df.copy()

if company:

    filtered = filtered[
        filtered["Company_Name"]
        .isin(company)
    ]

if status:

    filtered = filtered[
        filtered["Status"]
        .isin(status)
    ]

if plant:

    filtered = filtered[
        filtered["plantname"]
        .isin(plant)
    ]

if problem:

    filtered = filtered[
        filtered["Problem_Name"]
        .isin(problem)
    ]

# =====================================================
# KPI METRICS
# =====================================================

total = len(filtered)

resolved = len(
    filtered[
        filtered["Status"]
        .astype(str)
        .str.contains(
            "resolve",
            case=False
        )
    ]
)

pending = len(
    filtered[
        filtered["Status"]
        .astype(str)
        .str.contains(
            "pending",
            case=False
        )
    ]
)

closed = len(
    filtered[
        filtered["Status"]
        .astype(str)
        .str.contains(
            "close",
            case=False
        )
    ]
)

avg_hours = (
    filtered["ResolutionInHrs"]
    .fillna(0)
    .mean()
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {total:,}
    </div>

    <div class="metric-label">
    Total Complaints
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {resolved:,}
    </div>

    <div class="metric-label">
    Resolved
    </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {pending:,}
    </div>

    <div class="metric-label">
    Pending
    </div>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {closed:,}
    </div>

    <div class="metric-label">
    Closed
    </div>

    </div>
    """, unsafe_allow_html=True)

with c5:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {round(avg_hours,2)}
    </div>

    <div class="metric-label">
    Avg Resolution Hrs
    </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# CHART ROW 1
# =====================================================

left, right = st.columns(2)

# =====================================================
# STATUS DISTRIBUTION
# =====================================================

with left:

    st.markdown("""
    <div class="section-card">

    <h3>
    Complaint Status Distribution
    </h3>

    </div>
    """, unsafe_allow_html=True)

    status_df = (
        filtered["Status"]
        .value_counts()
        .reset_index()
    )

    status_df.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_df,
        values="Count",
        names="Status",
        hole=0.5
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# ROOT CAUSE
# =====================================================

with right:

    st.markdown("""
    <div class="section-card">

    <h3>
    Top Complaint Problems
    </h3>

    </div>
    """, unsafe_allow_html=True)

    top = (
        filtered["Problem_Name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top.columns = [
        "Problem",
        "Count"
    ]

    fig = px.bar(
        top,
        x="Count",
        y="Problem",
        orientation="h",
        text_auto=True
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CHART ROW 2
# =====================================================

left2, right2 = st.columns(2)

# =====================================================
# RESOLUTION ANALYSIS
# =====================================================

with left2:

    st.markdown("""
    <div class="section-card">

    <h3>
    Resolution Analysis by Plant
    </h3>

    </div>
    """, unsafe_allow_html=True)

    res = filtered[
        filtered["ResolutionInHrs"]
        .notna()
    ]

    plant_df = (
        res.groupby(
            "plantname"
        )["ResolutionInHrs"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        plant_df,
        x="plantname",
        y="ResolutionInHrs",
        text_auto=True
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TOP RESOLVERS
# =====================================================

with right2:

    st.markdown("""
    <div class="section-card">

    <h3>
    Top Resolvers
    </h3>

    </div>
    """, unsafe_allow_html=True)

    top_resolvers = (
        filtered["ResolvedBy"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_resolvers.columns = [
        "Resolver",
        "Count"
    ]

    fig = px.bar(
        top_resolvers,
        x="Count",
        y="Resolver",
        orientation="h",
        text_auto=True
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



