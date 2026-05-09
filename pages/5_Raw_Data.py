import streamlit as st
import pandas as pd
import numpy as np
from lib.data_ops import get_gaa_data_raw_search
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

st.write("The column \"AMT\" corresponds to the budget amount alloted, and has a unit of \"thousand pesos\"")

col1, col2 = st.columns(2)
with col1:
    searchterm = st.text_input("Search:")
    if searchterm != st.session_state["searchterm_raw"]:
        data_raw, numpages = get_gaa_data_raw_search(department, agency, searchterm = searchterm, page = 1)
        st.session_state["numpages_raw"] = numpages

with col2:
    page = st.selectbox("Page:",range(1,st.session_state["numpages_raw"]+1),width=100)
    if searchterm == st.session_state["searchterm_raw"]:
        data_raw, numpages = get_gaa_data_raw_search(department, agency, searchterm = searchterm, page = page)

st.session_state["searchterm_raw"] = searchterm

st.table(data_raw)