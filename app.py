import streamlit as st

st.set_page_config(
    page_title="Complaint Analytics",
    page_icon="📊",
    layout="wide"
)
st.title("Complaint Analytics Platform")

uploaded_file = st.sidebar.file_uploader(
    "Upload Complaint Excel",
    type=["xlsx"]
)

if uploaded_file:
    st.session_state["uploaded_file"] = uploaded_file
st.markdown("""
Welcome to Complaint Analytics Dashboard

Use the left menu to navigate.
""")