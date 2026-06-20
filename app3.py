import streamlit as st
import pandas as pd

from datetime import datetime

from streamlit_autorefresh import st_autorefresh

from auth import (
    login,
    is_authenticated,
    logout
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Complaint Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
GLOBAL
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #1e293b 100%
        );

    color: white;

    font-family:
        'Segoe UI',
        sans-serif;
}

/* =====================================================
REMOVE STREAMLIT PADDING
===================================================== */

.block-container {

    padding-top: 1.5rem;

    padding-left: 2rem;

    padding-right: 2rem;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {

    background:
        rgba(15,23,42,0.85);

    backdrop-filter: blur(18px);

    border-right:
        1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white;
}

/* =====================================================
LOGIN CONTAINER
===================================================== */

.login-container {

    margin-top: 120px;

    background:
        rgba(255,255,255,0.06);

    backdrop-filter: blur(18px);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 50px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.35);
}

/* =====================================================
TEXT INPUT
===================================================== */

.stTextInput input {

    background:
        rgba(255,255,255,0.08);

    border:
        1px solid rgba(255,255,255,0.08);

    color: white;

    border-radius: 12px;

    height: 50px;
}

/* =====================================================
BUTTON
===================================================== */

.stButton > button {

    width: 100%;

    height: 50px;

    border-radius: 12px;

    border: none;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #3b82f6
        );

    color: white;

    font-size: 16px;

    font-weight: 600;

    transition: 0.3s;
}

.stButton > button:hover {

    transform: scale(1.02);

    background:
        linear-gradient(
            90deg,
            #1d4ed8,
            #2563eb
        );
}

/* =====================================================
TOP NAVBAR
===================================================== */

.navbar {

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 20px;

    padding: 22px;

    margin-bottom: 25px;
}

/* =====================================================
TITLE
===================================================== */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: white;
}

/* =====================================================
SUBTITLE
===================================================== */

.subtitle {

    color: #94a3b8;

    margin-top: -10px;
}

/* =====================================================
METRIC CARDS
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
UPLOAD BOX
===================================================== */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,0.05);

    border-radius: 15px;

    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
#LOGIN SCREEN
# =====================================================

if not is_authenticated():

    st.markdown("""
    <style>

    [data-testid="stSidebar"] {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        st.markdown("""
        <div class="login-container">

        <h1 style="
            text-align:center;
            font-size:42px;
            margin-bottom:10px;
        ">
        📊 Complaint Analytics
        </h1>

        <p style="
            text-align:center;
            color:#94a3b8;
            margin-bottom:40px;
        ">
        Enterprise Complaint Management Platform
        </p>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if login(username, password):

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.stop()

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

# =====================================================
#SIDEBAR
# =====================================================

st.sidebar.success(
    f"👋 {st.session_state['username']}"
)

st.sidebar.info(
    f"""
⏳ Session Timeout

{minutes:02}:{seconds:02}
"""
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Complaint Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df

    st.sidebar.success(
        "File Uploaded"
    )

if st.sidebar.button("Logout"):

    logout()

    st.rerun()

# =====================================================
#NAVBAR
# =====================================================

st.markdown(f"""
<div class="navbar">

<div class="main-title">
Complaint Analytics Dashboard
</div>

<div style="
color:#94a3b8;
font-size:16px;
">

Real-time Monitoring System

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">

Monitor complaints, resolution trends,
aging analysis, and root cause patterns.

</div>
""", unsafe_allow_html=True)

# =====================================================
#RECENT COMPLAINTS
# =====================================================

st.markdown("""
<div class="section-card">

<h3>Recent Complaints</h3>

</div>
""", unsafe_allow_html=True)

if "df" in st.session_state:

    st.dataframe(
        st.session_state["df"].head(20),
        use_container_width=True,
        height=400
    )

else:

    st.info(
        "Upload a complaint Excel file to begin."
    )

