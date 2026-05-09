import streamlit as st
import pandas as pd
import numpy as np
from lib.data_ops import load_gaa_data
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

data_sub = load_gaa_data(department=department,agency=agency)
st.write("The column \"AMT\" corresponds to the budget amount alloted, and has a unit of \"thousand pesos\"")

col1, col2 = st.columns(2)
with col1:
    searchterm = st.text_input("Search:")
    if searchterm:
        str_cols = data_sub.select_dtypes(include="str").columns.to_list()
        search_filter = np.logical_or.reduce([data_sub[x].str.lower().str.contains(searchterm.lower()) for x in str_cols])
        data_sub = data_sub.loc[search_filter].reset_index(drop=True)

with col2:
    numitems = len(data_sub)
    numpages = (numitems+20-1)//20
    page = st.selectbox("Page:",range(1,numpages+1),width=100)

if numitems>0:
    st.table(data_sub.iloc[(page-1)*20:page*20])
else:
    st.table(data_sub)