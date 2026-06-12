import streamlit as st
import pandas as pd

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

st.title("Dataset Overview")

c1,c2,c3,c4=st.columns(4)
c1.metric("Total Records",len(df))
c2.metric("Companies",df["Company_Name"].nunique())
c3.metric("Plants",df["plantname"].nunique())
c4.metric("Products",df["Product_Name"].nunique())

st.divider()

st.subheader("Columns Information")
info=pd.DataFrame(
    {
        "Column":df.columns,
        "Datatype":[str(i) for i in df.dtypes],
    }
)
st.dataframe(info,use_container_width=True)

st.subheader("Missing Values")
missing=(df.isna().sum().reset_index())
missing.columns=[
    "Column",
    "Missing"
]

st.dataframe(
    missing.sort_values(
        "Missing",
        ascending=False
    ),
    use_container_width=True
)
