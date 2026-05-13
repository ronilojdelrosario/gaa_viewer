import streamlit as st
import pandas as pd
import plotly.express as px
from lib.data_ops import get_department_agencies_budget, get_departments_budgets, load_gaa_data_summary_deptagy, load_gaa_data_summary_forchart
from lib.utils import initialize_states

initialize_states()

######################################   Budget Distribution   ######################################
st.header("Budget Distribution", text_alignment = "center")

department= st.session_state["department"]
agency = st.session_state["agency"]

# Two-column set-up for the pie charts
col_1_1, col_1_2 = st.columns(2)

# Load agencies' budget for the selected department
agys_budgets = get_department_agencies_budget(department)
agys_budgets["AMT"] = 1000*agys_budgets["AMT"]      # Original data in thousands pesos

with col_1_1:   # Budget of agencies within the department
    st.subheader("Within Department", text_alignment = "center")
    # Pull = displace selected agency's pie for emphasis 
    pull_list = 0.05 * (agys_budgets.Agency == agency)
    # Plot
    fig_agy_dept = px.pie( agys_budgets, values = "AMT", names = "Agency",
                          height = 550, hole = 0.2, color_discrete_sequence = px.colors.qualitative.Prism )
    # Layout
    fig_agy_dept.update_traces( textposition = "inside", pull = pull_list, hovertemplate='Agency:  %{label}<br>AMT:        Php %{value:,d}', hoverlabel=dict(align="left"))
    fig_agy_dept.update_layout( legend = dict(yanchor = "top", y = -0.05, xanchor = "left", x = 0.05, maxheight = 0.2),
                                margin = dict(l = 30, r = 30, t = 0))
    
    st.plotly_chart(fig_agy_dept, key="agencies_dept")

# Load departments' budgets
depts_budgets = get_departments_budgets()
depts_budgets["AMT"] = 1000*depts_budgets["AMT"]

with col_1_2:
    st.subheader("Within Government", text_alignment = "center")

    pull_list = 0.05 * (depts_budgets.Department == department)

    fig_depts = px.pie( depts_budgets, values = "AMT", names = "Department",
                        height = 550, hole = 0.2, color_discrete_sequence = px.colors.qualitative.Antique)

    fig_depts.update_traces( textposition = "inside", pull = pull_list, hovertemplate='Department:  %{label}<br>AMT:                   Php %{value:,d}', hoverlabel=dict(align="left"))
    fig_depts.update_layout( legend = dict(yanchor = "top", y = -0.05, xanchor = "left", x = 0.05, maxheight = 0.2),
                             margin = dict(l = 30, r = 30, t = 0))
    
    st.plotly_chart(fig_depts, key="depts_all")

st.write("##")
st.write("##")

##################################   Budget Distribution By Type   ##################################

summary_dept_chart = load_gaa_data_summary_deptagy(department=department,type="purpose").drop(columns=["Total"]).melt(id_vars=["Name","UACS_AGY_DSC"],var_name="Expense Type",value_name="AMT")

st.header("Budget Distribution by Cost Structure and Expense Type", text_alignment = "center")

# Two-column set-up for the bar charts (for cost structure and for expense type)
col_2_1, col_2_2 = st.columns(2)

with col_2_1: # Budget per agency per cost structure
    summary_dept_chart1 = summary_dept_chart[["UACS_AGY_DSC", "Name", "AMT"]].groupby(["UACS_AGY_DSC", "Name"], as_index = False, sort=False).sum()
    # Plot
    fig_bar_agy_dept1 = px.bar(summary_dept_chart1, y = "UACS_AGY_DSC", x = "AMT", color = "Name", custom_data = ["Name"], orientation = 'h',
                        labels = {"Name":"Cost Structure"}, color_discrete_sequence = px.colors.qualitative.Antique,
                        height = 140 + 60*len(summary_dept_chart1.UACS_AGY_DSC.unique()) )
    # Layout
    fig_bar_agy_dept1.update_traces(hovertemplate='Agency:  %{y}<br>Type:       %{customdata[0]}<br>AMT:        Php %{x:,d}<extra></extra>', hoverlabel=dict(align="left"))
    fig_bar_agy_dept1.update_yaxes(ticklabelposition = "inside", title = None, ticklabelstandoff = 10, fixedrange = True)
    fig_bar_agy_dept1.update_xaxes(rangemode = "tozero", title = None, side = 'top', fixedrange = True, showticklabels = False)
    fig_bar_agy_dept1.update_layout( margin = dict(l = 0, r = 0, t = 140, b=0),
                                    legend = dict(yanchor = "top", y = 1, yref = 'container', xanchor = "left", x = 0, maxheight = 0.5))

    st.plotly_chart(fig_bar_agy_dept1, key="agencies_1")

with col_2_2: # Budget per agency per expense type
    summary_dept_chart2 = summary_dept_chart[["UACS_AGY_DSC", "Expense Type", "AMT"]].groupby(["UACS_AGY_DSC", "Expense Type"], as_index = False, sort=False).sum()
    # Plot
    fig_bar_agy_dept2 = px.bar(summary_dept_chart2, y = "UACS_AGY_DSC", x = "AMT", color = "Expense Type", custom_data = ["Expense Type"], orientation = 'h',
        color_discrete_sequence = px.colors.qualitative.Antique[7:], height = 140 + 60*len(summary_dept_chart2.UACS_AGY_DSC.unique()) )
    # Layout
    fig_bar_agy_dept2.update_traces(hovertemplate='Agency:  %{y}<br>Type:       %{customdata[0]}<br>AMT:        Php %{x:,d}<extra></extra>', hoverlabel=dict(align="left"))
    fig_bar_agy_dept2.update_yaxes(ticklabelposition = "inside", title = None, ticklabelstandoff = 10, fixedrange = True)
    fig_bar_agy_dept2.update_xaxes(rangemode = "tozero", title = None, side = 'top', fixedrange = True, showticklabels = False)
    fig_bar_agy_dept2.update_layout(margin = dict(l = 0, r = 0, t = 140, b = 0),
                                    legend = dict(yanchor = "top", y = 1, yref = 'container', xanchor = "left", x = 0, maxheight = 0.5))
    
    st.plotly_chart(fig_bar_agy_dept2, key="agencies_2")


st.write("##")
st.write("##")

##########################   Budget Distribution By Type (All Depts)   ##########################

summary_depts_all = load_gaa_data_summary_forchart()

st.header("All Departments", text_alignment = "center")

# Two-column set-up for the bar charts (for cost structure and for expense type)
col_3_1, col_3_2 = st.columns(2)

with col_3_1: # Budget per department per cost structure
    summary_depts_all_data1 = summary_depts_all[["UACS_DPT_DSC", "Name", "AMT"]].groupby(["UACS_DPT_DSC", "Name"], as_index = False, sort=False).sum()
    # Plot
    summary_depts_all_chart1 = px.bar(summary_depts_all_data1, y = "UACS_DPT_DSC", x = "AMT", color = "Name", custom_data = ["Name"], orientation = 'h',
                            labels = {"Name":"Cost Structure"}, color_discrete_sequence = px.colors.qualitative.Antique,
                            height = 140 + 30*len(summary_depts_all_data1.UACS_DPT_DSC.unique()) )
    # Layout
    summary_depts_all_chart1.update_traces(hovertemplate='Department:  %{y}<br>Type:                 %{customdata[0]}<br>AMT:                  Php %{x:,d}<extra></extra>', hoverlabel=dict(align="left"))
    summary_depts_all_chart1.update_yaxes(ticklabelposition = "inside", title = None, ticklabelstandoff = 10, fixedrange = True, autorange = "reversed")
    summary_depts_all_chart1.update_xaxes(rangemode = "tozero", title = None, side = 'top', fixedrange = True, showticklabels = False)
    summary_depts_all_chart1.update_layout( margin = dict(l = 0, r = 0, t = 140, b=0),
                                    legend = dict(yanchor = "top", y = 1, yref = 'container', xanchor = "left", x = 0, maxheight = 0.5))

    st.plotly_chart(summary_depts_all_chart1, key="depts_1")

with col_3_2: # Budget per department per expense type
    summary_depts_all_data2 = summary_depts_all[["UACS_DPT_DSC", "Expense Type", "AMT"]].groupby(["UACS_DPT_DSC", "Expense Type"], as_index = False, sort=False).sum()
    # Plot
    summary_depts_all_chart1 = px.bar(summary_depts_all_data2, y = "UACS_DPT_DSC", x = "AMT", color = "Expense Type", custom_data = ["Expense Type"],
                        orientation = 'h', color_discrete_sequence = px.colors.qualitative.Antique[7:],
                        height = 140 + 30*len(summary_depts_all_data2.UACS_DPT_DSC.unique()) )
    # Layout
    summary_depts_all_chart1.update_traces(hovertemplate='Department:  %{y}<br>Type:                 %{customdata[0]}<br>AMT:                  Php %{x:,d}<extra></extra>', hoverlabel=dict(align="left"))
    summary_depts_all_chart1.update_yaxes(ticklabelposition = "inside", title = None, ticklabelstandoff = 10, fixedrange = True, autorange = "reversed")
    summary_depts_all_chart1.update_xaxes(rangemode = "tozero", title = None, side = 'top', fixedrange = True, showticklabels = False)
    summary_depts_all_chart1.update_layout(margin = dict(l = 0, r = 0, t = 140, b = 0),
                                    legend = dict(yanchor = "top", y = 1, yref = 'container', xanchor = "left", x = 0, maxheight = 0.5))
    
    st.plotly_chart(summary_depts_all_chart1, key="depts_2")