import streamlit as st
from lib.data_ops import load_gaa_data
from lib.utils import initialize_states

st.set_page_config(layout="wide",page_title="GAA Viewer",page_icon=":ledger:")

initialize_states()

st.markdown(
    r"""
    <style>
    button[data-testid="stExpandSidebarButton"] {
            height: 2rem;
            width : 2rem;
            animation: bounce 2s ease infinite;
        }
    @keyframes bounce {
        70% { transform:translateY(0%); }
        80% { transform:translateY(-15%); }
        90% { transform:translateY(0%); }
        95% { transform:translateY(-7%); }
        97% { transform:translateY(0%); }
        99% { transform:translateY(-3%); }
        100% { transform:translateY(0); }
    }
    button[data-testid="stExpandSidebarButton"] span {
            font-size: 1.5em;
    }
    </style>
    """, unsafe_allow_html=True
)

data = load_gaa_data()

department = st.sidebar.selectbox("Department:",data.UACS_DPT_DSC.unique())
agencies = data.loc[data.UACS_DPT_DSC==department,"UACS_AGY_DSC"].unique()
agency = st.sidebar.selectbox("Agency:",agencies)

st.session_state["department"] = department
st.session_state["agency"] = agency

st.info("Use with caution. This is a rough draft. Raw data is from DBM website, but summary calculations are done by me.", icon="ℹ️")

pg = st.navigation([st.Page("pages//1_Agency_Budget.py"),st.Page("pages//2_Agency_Breakdown_By_Expense_Type.py"),st.Page("pages//3_Charts.py"),st.Page("pages//4_Agency_Highlights.py"),st.Page("pages//5_Raw_Data.py")])
pg.run()