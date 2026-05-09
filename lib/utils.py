import streamlit as st

def initialize_states():
    if "department" not in st.session_state:
        st.session_state["department"] = "Congress of the Philippines (CONGRESS)"
    if "agency" not in st.session_state:
        st.session_state["agency"] = "Senate"