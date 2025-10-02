import streamlit as st
import pandas as pd

def step1_upload_file():
    
    st.header("1️⃣ Charger le fichier des membres")
    
    uploaded_file = st.file_uploader("Sélectionnez le fichier Excel des membres", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success(f"✅ Fichier chargé avec succès! {len(df)} membres trouvés.")
            st.session_state.step = max(st.session_state.step, 2)
        except Exception as e:
            st.toast(
                f"Erreur lors du chargement du fichier: {e}",
                icon="❌",
                duration="long"
            )
    elif 'df' in st.session_state and st.session_state.df is not None:
        # File was deleted
        st.session_state.df = None
        st.session_state.selected_member = None
        st.session_state.step = 1
        st.info("ℹ️ Veuillez charger un fichier Excel.")