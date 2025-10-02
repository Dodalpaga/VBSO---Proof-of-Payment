import streamlit as st

def initialize_session_state():
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'columns_mapping' not in st.session_state:
        st.session_state.columns_mapping = {}
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'previous_selection' not in st.session_state:
        st.session_state.previous_selection = ""