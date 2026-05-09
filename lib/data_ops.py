import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

#########   Using Raw GAA Data   #########
@st.cache_data
def load_gaa_data_raw():
    filepath = Path(__file__).parent.parent / "data" / "gaa_data.parquet"
    data = pd.read_parquet(filepath)
    data.loc[pd.isna(data.UACS_DPT_DSC),"UACS_DPT_DSC"] = "Unspecified"
    data.loc[pd.isna(data.UACS_AGY_DSC),"UACS_AGY_DSC"] = "Unspecified"
    return data

@st.cache_data
def load_gaa_depts_agys():
    data = load_gaa_data_raw()
    return data[["UACS_DPT_DSC","UACS_AGY_DSC"]].drop_duplicates()

@st.cache_data(max_entries=10)
def load_gaa_data_raw_dptagy(department="",agency=""):
    data = load_gaa_data_raw()
    return data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)].drop(columns=["UACS_DPT_DSC","UACS_AGY_DSC"]).reset_index(drop=True)


@st.cache_data(max_entries=10)
def get_department_agencies_budget(department):
    data_all = load_gaa_data_raw()
    data = data_all.loc[data_all.UACS_DPT_DSC==department]
    # Either budget for specific agencies or for foreign-assisted projects
    data_sub = data.loc[(data.FUNDCD=="10101101")|(data.PREXC_FPAP_ID.str.get(6)=="3")]
    return data_sub[["UACS_AGY_DSC","AMT"]].rename(columns={"UACS_AGY_DSC":"Agency"}).groupby("Agency",as_index=False).sum()


@st.cache_data
def get_departments_budgets():
    data = load_gaa_data_raw()
    # Either budget for specific agencies or for foreign-assisted projects
    data_sub = data.loc[(data.FUNDCD=="10101101")|(data.PREXC_FPAP_ID.str.get(6)=="3")]
    return data_sub[["UACS_DPT_DSC","AMT"]].rename(columns={"UACS_DPT_DSC":"Department"}).groupby("Department",as_index=False).sum()

@st.cache_data(max_entries=10,show_spinner=False)
def get_gaa_data_wout_budget(department,agency,searchterm = "", page = 1,show_spinner=False):
    data = load_gaa_data_raw_dptagy(department=department,agency=agency)
    wout_budget = data.loc[(data.PREXC_LEVEL==7)&pd.isna(data.AMT)&(data.DSC.str.lower().str.contains(searchterm.lower()))].reset_index(drop=True)
    wout_budget["type"] = wout_budget.PREXC_FPAP_ID.str.get(6).map({"1":"Activity","2":"Locally-Funded Project","3":"Foreign-Assisted Project"})
    wout_budget["under"] = wout_budget.PREXC_FPAP_ID.str.get(0).map({"1":"General Administration and Support","2":"Support to Operations","3":"Operations"})
    numitems = len(wout_budget)
    numpages = (numitems+20-1)//20
    if numitems > 0:
        return wout_budget[["DSC","type","under"]].iloc[(page-1)*20:page*20], numpages
    else:
        return wout_budget[["DSC","type","under"]], 0
    
@st.cache_data(max_entries=10,show_spinner=False)
def get_gaa_data_raw_search(department,agency,searchterm = "", page = 1):
    data = load_gaa_data_raw_dptagy(department=department,agency=agency)
    str_cols = data.select_dtypes(include="str").columns.to_list()
    search_filter = np.logical_or.reduce([data[x].str.lower().str.contains(searchterm.lower()) for x in str_cols])
    data = data.loc[search_filter].reset_index(drop=True)
    numitems = len(data)
    numpages = (numitems+20-1)//20
    if numitems > 0:
        return data.iloc[(page-1)*20:page*20], numpages
    else:
        return data, 0


#########   Using GAA Summary Data   #########
@st.cache_data
def load_gaa_data_summary():
    filepath = Path(__file__).parent.parent / "data" / "gaa_data_summary.parquet"
    data = pd.read_parquet(filepath)
    return data

@st.cache_data(max_entries=10)
def load_gaa_data_summary_deptagy(department="",agency="",type=""):
    data = load_gaa_data_summary()

    if department!="" and agency!="":
        data = data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)]
        data.drop(columns=["UACS_DPT_DSC","UACS_AGY_DSC"],inplace=True)
    elif department!="":
        data = data.loc[data.UACS_DPT_DSC==department]
        data.drop(columns=["UACS_DPT_DSC"],inplace=True)

    if type!="":
        data = data.loc[data.type==type]
        data.drop(columns=["type"],inplace=True)

    return data.reset_index(drop=True)

@st.cache_data
def load_gaa_data_summary_forchart():
    data = load_gaa_data_summary()
    data = data.loc[data.type=="purpose"].reset_index(drop=True)
    return data.drop(columns=["Total","UACS_AGY_DSC","type"]).groupby(["Name","UACS_DPT_DSC"], as_index=False,
                    sort=False).sum().melt(id_vars=["Name","UACS_DPT_DSC"],var_name="Expense Type",value_name="AMT")

#########   Using GAA Expense Type Breakdown Data   #########
@st.cache_data
def load_gaa_data_exptype():
    filepath = Path(__file__).parent.parent / "data" / "gaa_data_exptype.parquet"
    data = pd.read_parquet(filepath)
    return data

@st.cache_data(max_entries=10)
def load_gaa_data_exptype_dptagy(department="",agency=""):
    data = load_gaa_data_exptype()
    return data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)].drop(columns=["UACS_DPT_DSC","UACS_AGY_DSC"]).reset_index(drop=True)