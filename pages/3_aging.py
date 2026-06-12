import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_data
uploaded_file = st.session_state.get(
    "uploaded_file",
    None
)
if uploaded_file:
    df = load_data(uploaded_file)
else:
    df=load_data("./ComplaintsData.xlsx")


st.title("Complaint Aging")

today = pd.Timestamp.today()

open_df = df[
    ~df["Status"]
     .astype(str)
     .str.contains(
         "resolve",
         case=False,
         na=False
     )
]

open_df["AgeDays"] = (
    today -
    open_df["LogedDate"]
).dt.days

def bucket(x):

    if x <= 1:
        return "Fresh"

    elif x <= 7:
        return "Moderate"

    elif x <= 30:
        return "Old"

    return "Critical"

open_df["Bucket"] = (
    open_df["AgeDays"]
    .apply(bucket)
)

bucket_df = (
    open_df["Bucket"]
    .value_counts()
    .reset_index()
)

bucket_df.columns=[
    "Bucket",
    "Count"
]

fig = px.pie(
    bucket_df,
    values="Count",
    names="Bucket"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    open_df.sort_values(
        "AgeDays",
        ascending=False
    ),
    use_container_width=True
)