import streamlit as st
import pandas as pd
from datetime import datetime
from utils.loader import load_data
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
# PAGE CONFIG UI
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
PAGE TITLE
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

    font-size: 38px;

    font-weight: 700;

    color: white;
}

/* =====================================================
METRIC LABEL
===================================================== */

.metric-label {

    color: #94a3b8;

    margin-top: 10px;

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
TABLE
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
📊 Dataset Overview
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-subtitle">

Understand the structure, quality,
and completeness of complaint data.

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
# KPI CARDS
# =====================================================
total_records = len(df)

companies = (
    df["Company_Name"].nunique()
    if "Company_Name" in df.columns
    else 0
)

plants = (
    df["plantname"].nunique()
    if "plantname" in df.columns
    else 0
)

products = (
    df["Product_Name"].nunique()
    if "Product_Name" in df.columns
    else 0
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {total_records:,}
    </div>

    <div class="metric-label">
    Total Records
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {companies:,}
    </div>

    <div class="metric-label">
    Companies
    </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {plants:,}
    </div>

    <div class="metric-label">
    Plants
    </div>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-value">
    {products:,}
    </div>

    <div class="metric-label">
    Products
    </div>

    </div>
    """, unsafe_allow_html=True)
    
    
# =====================================================
# COLUMN INFO
# =====================================================

st.markdown("""
<div class="section-card">

<h3>
🧾 Columns Information
</h3>

</div>
""", unsafe_allow_html=True)

info = pd.DataFrame(
    {
        "Column": df.columns,

        "Datatype": [
            str(i)
            for i in df.dtypes
        ],

        "Non Null Count": [
            df[col].notna().sum()
            for col in df.columns
        ],

        "Unique Values": [
            df[col].nunique()
            for col in df.columns
        ]
    }
)

st.dataframe(
    info,
    use_container_width=True,
    height=400
)

# =====================================================
# MISSING VALUES
# =====================================================

st.markdown("""
<div class="section-card">

<h3>
⚠️ Missing Values Analysis
</h3>

</div>
""", unsafe_allow_html=True)

missing = (
    df.isna()
    .sum()
    .reset_index()
)

missing.columns = [
    "Column",
    "Missing Values"
]

missing["Missing %"] = (
    (
        missing["Missing Values"]
        / len(df)
    ) * 100
).round(2)

missing = missing.sort_values(
    "Missing Values",
    ascending=False
)

st.dataframe(
    missing,
    use_container_width=True,
    height=400
)

# st.divider()

# st.subheader("Columns Information")
# info=pd.DataFrame(
#     {
#         "Column":df.columns,
#         "Datatype":[str(i) for i in df.dtypes],
#     }
# )
# st.dataframe(info,use_container_width=True)

# st.subheader("Missing Values")
# missing=(df.isna().sum().reset_index())
# missing.columns=[
#     "Column",
#     "Missing"
# ]

# st.dataframe(
#     missing.sort_values(
#         "Missing",
#         ascending=False
#     ),
#     use_container_width=True
# )
