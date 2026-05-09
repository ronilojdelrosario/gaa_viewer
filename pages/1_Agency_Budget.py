import streamlit as st
import pandas as pd
import plotly.express as px
from lib.data_ops import load_gaa_data_summary
from lib.utils import initialize_states

initialize_states()

department= st.session_state["department"]
agency = st.session_state["agency"]

summary = load_gaa_data_summary(department, agency)

st.write(f"Total new appropriations: Php {int(summary.loc[summary.Name=="Total New Appropriations","Total"].values[0]):,d}")

st.subheader("Budget Distribution by Type", text_alignment="center")

summary_pie = summary.loc[summary.type=="purpose"].drop(columns=["Total"]).melt(id_vars=["Name","type"],var_name="Expense Type",value_name="AMT")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(summary_pie,values="AMT",names="Name",hole=0.3,category_orders={"Name":["GAS","STO","Ops","LFPs","FAPs"]},height=450,
                  color_discrete_sequence = px.colors.qualitative.Prism)
    fig1.update_traces(textposition="inside")
    fig1.update_layout(legend=dict(yanchor="top",y=-0.05,xanchor="center",x=0.5,maxheight=1),
                        margin=dict(l=15,r=15,t=0,b=150))
    st.plotly_chart(fig1)
with col2:
    fig2 = px.pie(summary_pie,values="AMT",names="Expense Type",hole=0.3,height=450,
                  color_discrete_sequence = px.colors.qualitative.Antique)
    fig2.update_traces(textposition="inside")
    fig2.update_layout(legend=dict(yanchor="top",y=-0.05,xanchor="center",x=0.5,maxheight=1),
                        margin=dict(l=15,r=15,t=0,b=150))
    st.plotly_chart(fig2)

pill = st.pills("Up to:",["Cost structure","Programs","Subprograms","Activities"],default="Cost structure")

formatting = {"group":"font-variant:small-caps; padding-left: 0; padding-top:1.5em;","purpose":"padding-left: 1em;","program":"padding-left: 2em;","sum":"padding-left: 1em;","total_sum":"padding-left: 0; padding-top:1em;","activity":"padding-left: 2em;","activity_program":"padding-left: 3em;","activity_subprogram":"padding-left: 4em;","subprogram":"padding-left: 3em;","project":"padding-left: 2em;"}

format_dict={
    "group" : ["font-variant:small-caps; padding-left: 0.2em; padding-top:1.5em; background-color: rgba(255,116,108,0.4);"] + ["padding-top:1.5em; background-color: rgba(255,116,108,0.4);"]*5,
    "purpose" : ["padding-left: 1em; background-color: rgba(255,116,108,0.2);"] + ["background-color: rgba(255,116,108,0.2);"]*5,
    "program" : ["padding-left: 2em; background-color: rgba(255,116,108,0.1);"] + ["background-color: rgba(255,116,108,0.1);"]*5,
    "subprogram": ["padding-left: 3em; background-color: rgba(255,116,108,0.05);"] + ["background-color: rgba(255,116,108,0.05);"]*5,
    "sum" : ["padding-left: 1em; background-color: rgba(72,202,228,0.25);"] + ["background-color: rgba(72,202,228,0.25);"]*5,
    "total_sum" : ["padding-left: 0.2em; padding-top:1em; background-color: rgba(72,202,228,0.5);"] + ["padding-top:1em; background-color: rgba(72,202,228,0.5);"]*5,
    "activity" : ["padding-left: 2em;"] + [""]*5,
    "activity_program" : ["padding-left: 3em;"] + [""]*5,
    "activity_subprogram" : ["padding-left: 4em;"] + [""]*5,
    "project" :["padding-left: 2em;"] + [""]*5
}

summary_todisplay = summary.loc[(summary.type.isin(["group"]))|(summary.Total>0)].reset_index(drop=True)
if summary.loc[summary.Name=="Total, Project(s)","Total"].values[0] ==0:
    summary_todisplay = summary_todisplay.loc[summary_todisplay.Name!="B. Project(s)"].reset_index(drop=True)

if pill == "Cost structure":
    summary_todisplay = summary_todisplay.loc[~summary_todisplay.type.isin(["program","subprogram","activity","activity_program","activity_subprogram","project"])].reset_index(drop=True)
elif pill == "Programs":
    summary_todisplay = summary_todisplay.loc[~summary_todisplay.type.isin(["subprogram","activity","activity_program","activity_subprogram","project"])].reset_index(drop=True)
elif pill == "Subprograms":
    summary_todisplay = summary_todisplay.loc[~summary_todisplay.type.isin(["activity","activity_program","activity_subprogram","project"])].reset_index(drop=True)

formatting_temp = summary_todisplay.type.map(format_dict)
formatting_df = pd.DataFrame(formatting_temp.tolist(),columns=summary_todisplay.drop(columns=["type"]).columns).rename(columns={"Name":""})

st.table(summary_todisplay.drop(columns=["type"]).rename(columns={"Name":""}).style.apply(lambda s: formatting_df,axis=None).format(formatter = lambda x: ' ' if (x==0 or pd.isna(x)) else (x if isinstance(x,str) else f"{int(x):,d}"),thousands=",").set_properties(subset=["Personnel Services","Maintenance and Other Operating Expenses","Financial Expenses","Capital Outlays","Total"],width="100px"),border='horizontal')