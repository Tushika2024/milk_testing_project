import streamlit as st

from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode
)

from utils.loader import load_data

uploaded_file = st.session_state.get(
    "uploaded_file",
    None
)
if uploaded_file:
    df = load_data(uploaded_file)
else:
    df=load_data("./ComplaintsData.xlsx")

st.title(
    "Complaint Explorer"
)

gb = (
    GridOptionsBuilder
    .from_dataframe(df)
)

gb.configure_selection(
    selection_mode="single",
    use_checkbox=True
)

grid = AgGrid(
    df,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=500
)

selected = grid["selected_rows"]

if selected is not None and not selected.empty:

    row = selected.iloc[0]

    st.subheader(
        "Complaint Details"
    )

    st.write(
        f"### Complaint ID : {row['ComplainId']}"
    )

    st.write(
        f"**Company:** {row['Company_Name']}"
    )

    st.write(
        f"**Plant:** {row['plantname']}"
    )

    st.write(
        f"**Product:** {row['Product_Name']}"
    )

    st.write(
        f"**Problem:** {row['Problem_Name']}"
    )

    st.write(
        f"**Status:** {row['Status']}"
    )

    st.write(
        f"**Remark:** {row['Remark']}"
    )

    st.write(
        f"**Solution:** {row['Solution']}"
    )

    st.write(
        f"**Logged By:** {row['LoggedBy']}"
    )

    st.write(
        f"**Resolved By:** {row['ResolvedBy']}"
    )