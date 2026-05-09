import pandas as pd
import streamlit as st

from lib.data_ops import load_gaa_data_summary_deptagy, get_gaa_data_wout_budget
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

#######################   Highest stuff   #######################
st.header("Highest budget per type")

summary = load_gaa_data_summary_deptagy(department, agency)

df_list = []

# Total
df_list.append(pd.DataFrame([["Total:"]],columns=["Name"]))
df_list.append(summary.loc[summary.Name=="Total New Appropriations"].drop(columns=["type"]).reset_index(drop=True))
# Highest cost structure
df_list.append(pd.DataFrame([["Highest budget (group):"]],columns=["Name"]))
df_list.append(summary.loc[(summary.type=="purpose")].drop(columns=["type"]).sort_values("Total",ascending=False).head(1).reset_index(drop=True))
# Highest program
df_list.append(pd.DataFrame([["Highest budget (program):"]],columns=["Name"]))
df_list.append(summary.loc[(summary.type=="program")].drop(columns=["type"]).sort_values("Total",ascending=False).head(1).reset_index(drop=True))
# Highest activity
df_list.append(pd.DataFrame([["Highest budget (activities - regular programs):"]],columns=["Name"]))
df_list.append(summary.loc[(summary.type.str.startswith("activity"))].drop(columns=["type"]).sort_values("Total",ascending=False).head(3).reset_index(drop=True))
# Highest project
df_list.append(pd.DataFrame([["Highest budget (projects):"]],columns=["Name"]))
df_list.append(summary.loc[(summary.type=="project")].drop(columns=["type"]).sort_values("Total",ascending=False).head(3).reset_index(drop=True))

df = pd.concat(df_list).reset_index(drop=True)

formatting = df.Total.apply(lambda x: "padding-left: 2em; padding-bottom:0.5em;" if x>0 else "padding: 1em 0.5em 0.5em 0.25em; text-transform: uppercase;").rename("Name")

st.table(df.style.apply(lambda s: formatting).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=","),border=False)

#######################   No budget allocated   #######################
st.header("Line items without allocated budget")

col1, col2 = st.columns(2)
with col1:
    searchterm = st.text_input("Search:")
    if searchterm != st.session_state["searchterm_woutbudget"]:
        data_woutbudget, numpages = get_gaa_data_wout_budget(department, agency, searchterm = searchterm, page = 1)
        st.session_state["numpages_woutbudget"] = numpages

with col2:
    page = st.selectbox("Page:",range(1,st.session_state["numpages_woutbudget"]+1),width=100)
    if searchterm == st.session_state["searchterm_woutbudget"]:
        data_woutbudget, numpages = get_gaa_data_wout_budget(department, agency, searchterm = searchterm, page = page)

st.session_state["searchterm_woutbudget"] = searchterm

st.table(data_woutbudget)