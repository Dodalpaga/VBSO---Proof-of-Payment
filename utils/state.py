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
    if 'show_uploader' not in st.session_state:
        st.session_state.show_uploader = False
    if 'show_config' not in st.session_state:
        st.session_state.show_config = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Accueil"
    if 'pending_toasts' not in st.session_state:
        st.session_state.pending_toasts = []