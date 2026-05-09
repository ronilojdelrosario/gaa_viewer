import pandas as pd
import streamlit as st

from lib.data_ops import load_gaa_data_summary, load_gaa_data

department= st.session_state["department"]
agency = st.session_state["agency"]

#######################   Highest stuff   #######################
st.header("Highest budget per type")

summary = load_gaa_data_summary(department, agency)

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

raw = load_gaa_data()
raw_dept = raw.loc[(raw.UACS_DPT_DSC==department)&(raw.UACS_AGY_DSC==agency)]
wout_budget = raw_dept.loc[(raw.PREXC_LEVEL==7)&pd.isna(raw.AMT)].reset_index(drop=True)
wout_budget["type"] = wout_budget.PREXC_FPAP_ID.str.get(6).map({"1":"Activity","2":"Locally-Funded Project","3":"Foreign-Assisted Project"})
wout_budget["under"] = wout_budget.PREXC_FPAP_ID.str.get(0).map({"1":"General Administration and Support","2":"Support to Operations","3":"Operations"})

col1, col2 = st.columns(2)
with col1:
    searchterm = st.text_input("Search:")
    if searchterm:
        wout_budget = wout_budget.loc[wout_budget.DSC.str.lower().str.contains(searchterm.lower())].reset_index(drop=True)

with col2:
    numitems = len(wout_budget)
    numpages = (numitems+20-1)//20
    page = st.selectbox("Page:",range(1,numpages+1),width=100)

if numitems>0:
    st.table(wout_budget[["DSC","type","under"]].iloc[(page-1)*20:page*20])
else:
    st.table(wout_budget[["DSC","type","under"]])