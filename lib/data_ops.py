import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_gaa_data(department="",agency=""):
    filepath = Path(__file__).parent.parent / "data" / "gaa_data.parquet"
    data = pd.read_parquet(filepath)
    data.loc[pd.isna(data.UACS_DPT_DSC),"UACS_DPT_DSC"] = "Unspecified"
    data.loc[pd.isna(data.UACS_AGY_DSC),"UACS_AGY_DSC"] = "Unspecified"
    if department!="" and agency!="":
        data = data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)]
    return data

@st.cache_data
def load_gaa_data_summary(department="",agency="",type=""):
    filepath = Path(__file__).parent.parent / "data" / "gaa_data_summary.parquet"
    data = pd.read_parquet(filepath)
    if department!="" and agency!="":
        data = data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)]
        data.drop(columns=["UACS_DPT_DSC","UACS_AGY_DSC"],inplace=True)
    elif department!="":
        data = data.loc[data.UACS_DPT_DSC==department]
        data.drop(columns=["UACS_DPT_DSC"],inplace=True)

    if type!="":
        data = data.loc[data.type==type]
        data.drop(columns=["type"],inplace=True)
    return data

@st.cache_data
def load_gaa_data_summary_forchart():
    data = load_gaa_data_summary(type="purpose")
    return data.drop(columns=["Total","UACS_AGY_DSC"]).groupby(["Name","UACS_DPT_DSC"], as_index=False,
                    sort=False).sum().melt(id_vars=["Name","UACS_DPT_DSC"],var_name="Expense Type",value_name="AMT")

@st.cache_data
def load_gaa_data_exptype(department="",agency=""):
    filepath = Path(__file__).parent.parent / "data" / "gaa_data_exptype.parquet"
    data = pd.read_parquet(filepath)
    if department!="" and agency!="":
        data = data.loc[(data.UACS_DPT_DSC==department)&(data.UACS_AGY_DSC==agency)]
        data.drop(columns=["UACS_DPT_DSC","UACS_AGY_DSC"],inplace=True)
    return data

@st.cache_data
def get_department_agencies_budget(department):
    data_all = load_gaa_data()
    data = data_all.loc[data_all.UACS_DPT_DSC==department]
    # Either budget for specific agencies or for foreign-assisted projects
    data_sub = data.loc[(data.FUNDCD=="10101101")|(data.PREXC_FPAP_ID.str.get(6)=="3")]
    return data_sub[["UACS_AGY_DSC","AMT"]].rename(columns={"UACS_AGY_DSC":"Agency"}).groupby("Agency",as_index=False).sum()

@st.cache_data
def get_departments_budgets():
    data = load_gaa_data()
    # Either budget for specific agencies or for foreign-assisted projects
    data_sub = data.loc[(data.FUNDCD=="10101101")|(data.PREXC_FPAP_ID.str.get(6)=="3")]
    return data_sub[["UACS_DPT_DSC","AMT"]].rename(columns={"UACS_DPT_DSC":"Department"}).groupby("Department",as_index=False).sum()