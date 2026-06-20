import pandas as pd
import  numpy as np
import streamlit as st
from db import get_connection

@st.cache_data
def load_data(uploaded_file):
    # conn=get_connection()
    # query= "SELECT * FROM complaints"
    # df=pd.read_sql(query,conn)
    # conn.close()
    # if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    # else:
    #     df=pd.read_excel(filepath)
        
    date_cols=["LogedDate","resolveDate"]
    for col in date_cols:
            if col in df.columns:
                df[col]=pd.to_datetime(df[col],errors="coerce") #value that cannot be converted to the target data type, don't crash.force it to become a missing value (NaN)
    return df