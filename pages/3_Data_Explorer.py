import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from auth import is_authenticated,logout

from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode
)

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
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Complaint Explorer",
    page_icon="🔍",
    layout="wide"
)

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
SEARCH BOX
===================================================== */

.stTextInput input {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    color: white;

    border-radius: 12px;

    height: 48px;
}

/* =====================================================
CARD
===================================================== */

.card {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 20px;

    padding: 25px;

    margin-top: 20px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.25);
}

/* =====================================================
DETAIL LABEL
===================================================== */

.detail-label {

    color: #94a3b8;

    font-size: 14px;

    margin-bottom: 5px;
}

/* =====================================================
DETAIL VALUE
===================================================== */

.detail-value {

    color: white;

    font-size: 18px;

    font-weight: 600;

    margin-bottom: 18px;
}

/* =====================================================
GRID
===================================================== */

.ag-theme-streamlit {

    --ag-background-color:
        rgba(255,255,255,0.03);

    --ag-foreground-color: white;

    --ag-header-background-color:
        rgba(255,255,255,0.06);

    --ag-border-color:
        rgba(255,255,255,0.08);

    --ag-row-hover-color:
        rgba(255,255,255,0.06);

    border-radius: 18px;
}

/* =====================================================
SECTION TITLE
===================================================== */

.section-title {

    font-size: 24px;

    font-weight: 600;

    color: white;

    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="page-title">
🔍 Complaint Explorer
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-subtitle">

Search, filter, and inspect detailed
complaint records across the organization.

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
# SEARCH BAR
# =====================================================

search = st.text_input(
    "Search Complaints"
)

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

# =====================================================
# AGGRID CONFIG
# =====================================================

st.markdown("""
<div class="card">

<div class="section-title">
📋 Complaint Records
</div>

</div>
""", unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(
    filtered_df
)

# =====================================================
# COLUMN CONFIG
# =====================================================

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True,
    floatingFilter=True
)

# =====================================================
# PAGINATION
# =====================================================

gb.configure_pagination(
    paginationAutoPageSize=False,
    paginationPageSize=20
)

# =====================================================
# SELECTION
# =====================================================

gb.configure_selection(
    selection_mode="single",
    use_checkbox=True
)

# =====================================================
# CUSTOM ROW STYLE
# =====================================================

cellsytle_jscode = JsCode("""
function(params) {

    if (params.value == 'Pending') {
        return {
            'color': '#facc15',
            'fontWeight': '600'
        }
    }

    if (params.value == 'Resolved') {
        return {
            'color': '#22c55e',
            'fontWeight': '600'
        }
    }

    if (params.value == 'Closed') {
        return {
            'color': '#3b82f6',
            'fontWeight': '600'
        }
    }
}
""")

gb.configure_column(
    "Status",
    cellStyle=cellsytle_jscode
)

grid_options = gb.build()

# =====================================================
# GRID TABLE
# =====================================================

grid = AgGrid(
    filtered_df,

    gridOptions=grid_options,

    update_mode=GridUpdateMode.SELECTION_CHANGED,

    fit_columns_on_grid_load=True,

    allow_unsafe_jscode=True,

    theme="streamlit",

    height=500
)

# =====================================================
# SELECTED ROW
# =====================================================

selected = grid["selected_rows"]

# =====================================================
# DETAILS PANEL
# =====================================================

if selected is not None and len(selected) > 0:

    row = pd.DataFrame(selected).iloc[0]

    st.markdown("""
    <div class="card">

    <div class="section-title">
    🧾 Complaint Details
    </div>

    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)

    # =====================================================
    # LEFT DETAILS
    # =====================================================

    with left:

        st.markdown(f"""
        <div class="detail-label">
        Complaint ID
        </div>

        <div class="detail-value">
        {row['ComplainId']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Company
        </div>

        <div class="detail-value">
        {row['Company_Name']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Plant
        </div>

        <div class="detail-value">
        {row['plantname']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Product
        </div>

        <div class="detail-value">
        {row['Product_Name']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Problem
        </div>

        <div class="detail-value">
        {row['Problem_Name']}
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # RIGHT DETAILS
    # =====================================================

    with right:

        st.markdown(f"""
        <div class="detail-label">
        Status
        </div>

        <div class="detail-value">
        {row['Status']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Logged By
        </div>

        <div class="detail-value">
        {row['LoggedBy']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Resolved By
        </div>

        <div class="detail-value">
        {row['ResolvedBy']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detail-label">
        Resolution Hours
        </div>

        <div class="detail-value">
        {row['ResolutionInHrs']}
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # REMARK
    # =====================================================

    st.markdown("""
    <div class="card">

    <div class="section-title">
    📝 Remarks & Solution
    </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(f"""
        <div class="detail-label">
        Remark
        </div>

        <div class="detail-value">
        {row['Remark']}
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="detail-label">
        Solution
        </div>

        <div class="detail-value">
        {row['Solution']}
        </div>
        """, unsafe_allow_html=True)

