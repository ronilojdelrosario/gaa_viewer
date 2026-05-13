import streamlit as st
import pandas as pd
from lib.data_ops import load_gaa_data_exptype_dptagy
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

data = load_gaa_data_exptype_dptagy(department,agency)
formatting_series = data["AMT"].map(lambda x: "padding-left:0; padding-top:1em;" if pd.isna(x) else "padding-left:1em").rename("Name")
ps_ind = data.loc[data.Name=="Personnel Services"].index.values
mooe_ind = data.loc[data.Name=="Maintenance and Other Operating Expenses"].index.values
co_ind = data.loc[data.Name=="Capital Outlays"].index.values
fe_ind = data.loc[data.Name=="Financial Expenses"].index.values

colcounts = 0
for x in [ps_ind,mooe_ind,co_ind]:
    if len(x)>0:
        colcounts+=1

cols = st.columns(colcounts)
col_ind = 0

if len(ps_ind) > 0:
    with cols[col_ind]:
        if len(mooe_ind) > 0:
            st.table(data.iloc[ps_ind[0]:mooe_ind[0]].style.apply(lambda s: formatting_series.iloc[ps_ind[0]:mooe_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        elif len(co_ind) > 0:
            st.table(data.iloc[ps_ind[0]:co_ind[0]].style.apply(lambda s: formatting_series.iloc[ps_ind[0]:co_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        elif len(fe_ind) > 0:
            st.table(data.iloc[ps_ind[0]:fe_ind[0]].style.apply(lambda s: formatting_series.iloc[ps_ind[0]:fe_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        else:
            st.table(data.iloc[ps_ind[0]:].style.apply(lambda s: formatting_series.iloc[ps_ind[0]:]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
    col_ind += 1

if len(mooe_ind) > 0:
    with cols[col_ind]:
        if len(fe_ind) > 0:
            st.table(data.iloc[mooe_ind[0]:fe_ind[0]].style.apply(lambda s: formatting_series.iloc[mooe_ind[0]:fe_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        elif len(co_ind) > 0:
            st.table(data.iloc[mooe_ind[0]:co_ind[0]].style.apply(lambda s: formatting_series.iloc[mooe_ind[0]:co_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        else:
            st.table(data.iloc[mooe_ind[0]:].style.apply(lambda s: formatting_series.iloc[mooe_ind[0]:]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
    col_ind += 1

if len(co_ind) > 0:
    with cols[col_ind]:
        st.table(data.iloc[co_ind[0]:].style.apply(lambda s: formatting_series.iloc[co_ind[0]:]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)

if len(fe_ind) > 0:
    with cols[-1]:
        if len(co_ind) >0:
            st.table(data.iloc[fe_ind[0]:co_ind[0]].style.apply(lambda s: formatting_series.iloc[fe_ind[0]:co_ind[0]]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)
        else:
            st.table(data.iloc[fe_ind[0]:].style.apply(lambda s: formatting_series.iloc[fe_ind[0]:]).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True,hide_header=True)


#with st.container(horizontal_alignment="center"):
#    st.table(data.style.apply(lambda s: formatting_series).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Name","AMT"],width="200px"),width="content",border='horizontal',hide_index=True)