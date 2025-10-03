import streamlit as st
import pandas as pd
from utils.toast_manager import add_persistent_toast

def step1_upload_file():
    
    st.header("1️⃣ Charger le fichier des membres accessible depuis SportEasy")
    
    # Si un fichier est déjà chargé, afficher un résumé et permettre de le remplacer
    if st.session_state.df is not None:
        st.success(f"✅ Fichier chargé: {len(st.session_state.df)} membres trouvés.")
        
        # Option pour voir un aperçu
        with st.expander("📊 Voir un aperçu des données"):
            st.dataframe(st.session_state.df.head(10))
        
        # Option pour recharger un nouveau fichier
        if st.button("🔄 Charger un nouveau fichier", type="secondary"):
            st.session_state.show_uploader = True
            st.rerun()
        
        # Si l'utilisateur a cliqué pour recharger
        if 'show_uploader' not in st.session_state:
            st.session_state.show_uploader = False
            
        if st.session_state.show_uploader:
            st.warning("⚠️ Charger un nouveau fichier réinitialisera la configuration des colonnes.")
            uploaded_file = st.file_uploader(
                "Sélectionnez le fichier Excel des membres", 
                type=['xlsx', 'xls'],
                key="file_uploader_replace"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state.df = df
                    st.session_state.columns_mapping = {}  # Réinitialiser le mapping
                    st.session_state.step = 2
                    st.session_state.show_uploader = False
                    st.success(f"✅ Nouveau fichier chargé avec succès! {len(df)} membres trouvés.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur lors du chargement du fichier: {e}")
    else:
        # Premier chargement
        uploaded_file = st.file_uploader(
            "Sélectionnez le fichier Excel des membres accessible depuis SportEasy", 
            type=['xlsx', 'xls'], 
            label_visibility="hidden"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state.df = df
                st.success(f"✅ Fichier chargé avec succès! {len(df)} membres trouvés.")
                st.session_state.step = max(st.session_state.step, 2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier: {e}")