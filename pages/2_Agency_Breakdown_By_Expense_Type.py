import streamlit as st
import pandas as pd
from lib.data_ops import load_gaa_data_exptype
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

data = load_gaa_data_exptype(department,agency)
formatting_series = data["AMT"].map(lambda x: "padding-left:0; padding-top:1em;" if pd.isna(x) else "padding-left:1em").rename("Name")

st.table(data.style.apply(lambda s: formatting_series).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=","),border='horizontal')