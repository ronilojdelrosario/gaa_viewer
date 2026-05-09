import streamlit as st

def initialize_states():
    if "department" not in st.session_state:
        st.session_state["department"] = "Congress of the Philippines (CONGRESS)"
    if "agency" not in st.session_state:
        st.session_state["agency"] = "Senate"
    if "searchterm_woutbudget" not in st.session_state:
        st.session_state["searchterm_woutbudget"] = None
    if "numpages_woutbudget" not in st.session_state:
        st.session_state["numpages_woutbudget"] = 100
    if "searchterm_raw" not in st.session_state:
        st.session_state["searchterm_raw"] = None
    if "numpages_raw" not in st.session_state:
        st.session_state["numpages_raw"] = 100