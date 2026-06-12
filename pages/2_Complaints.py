import streamlit as st
import plotly.express as px

from utils.loader import load_data
filepath="./ComplaintsData.xlsx"
uploaded_file = st.session_state.get(
    "uploaded_file",
    None
)
if uploaded_file:
    df=load_data(uploaded_file)
else:
    df=load_data(filepath)

st.title("Complaint Dashboard")

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

avg_hours = (
    filtered["ResolutionInHrs"]
    .fillna(0)
    .mean()
)

c1,c2,c3 = st.columns(3)

c1.metric(
    "Total",
    total
)

c2.metric(
    "Resolved",
    resolved
)

c3.metric(
    "Avg Hours",
    round(avg_hours,2)
)

status_df = (
    filtered["Status"]
    .value_counts()
    .reset_index()
)

status_df.columns=[
    "Status",
    "Count"
]

fig = px.pie(
    status_df,
    values="Count",
    names="Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#resolution analysis
st.subheader(
    "Resolution Analysis"
)

res = df[
    df["ResolutionInHrs"]
    .notna()
]

plant = (
    res.groupby(
        "plantname"
    )["ResolutionInHrs"]
    .mean()
    .reset_index()
)

fig = px.bar(
    plant,
    x="plantname",
    y="ResolutionInHrs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#root cause 
st.subheader(
    "Root Cause Analysis"
)

top = (
    df["Problem_Name"]
    .value_counts()
    .head(20)
    .reset_index()
)

top.columns=[
    "Problem",
    "Count of Complaints"
]

fig = px.bar(
    top,
    x="Count of Complaints",
    y="Problem",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)