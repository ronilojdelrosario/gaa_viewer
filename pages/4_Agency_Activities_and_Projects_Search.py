import pandas as pd
import streamlit as st

from lib.data_ops import load_gaa_data_summary_deptagy, get_gaa_data_wout_budget
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

st.header("Activities/projects search")

col1, col2, col3 = st.columns([4,1,1])
with col1:
    searchterm = st.text_input("Search:")
    if searchterm != st.session_state["searchterm_woutbudget"]:
        st.session_state["filter_woutbudget"] = None

with col2:
    typefilter = st.selectbox("Include:",["With Budget","Without Budget"], width=200)
    if typefilter != st.session_state["filter_woutbudget"]:
        data_woutbudget, numpages = get_gaa_data_wout_budget(department, agency, searchterm = searchterm, page = 1, typefilter = typefilter)
        st.session_state["numpages_woutbudget"] = numpages

with col3:
    page = st.selectbox("Page:",range(1,st.session_state["numpages_woutbudget"]+1),width=100)
    if searchterm == st.session_state["searchterm_woutbudget"]:
        data_woutbudget, numpages = get_gaa_data_wout_budget(department, agency, searchterm = searchterm, page = page, typefilter = typefilter)

st.session_state["searchterm_woutbudget"] = searchterm

st.table(data_woutbudget.style.format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=","))