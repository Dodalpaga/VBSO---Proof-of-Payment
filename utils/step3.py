import streamlit as st
import pandas as pd

def step3_search_member():
    
    st.header("3️⃣ Rechercher un membre")
    
    df = st.session_state.df
    mapping = st.session_state.columns_mapping
    
    # Créer une colonne de recherche combinée et une liste pour l'autocomplétion
    df['_search'] = (df[mapping["Nom"]].astype(str).str.lower() + " " + 
                     df[mapping["Prénom"]].astype(str).str.lower())
    df['_display'] = (df[mapping["Nom"]].astype(str).str.upper() + " " + 
                      df[mapping["Prénom"]].astype(str).str.capitalize())
    
    # Créer la liste des options pour l'autocomplétion
    membre_options = df['_display'].tolist()
    membre_dict = {display: idx for idx, display in zip(df.index, df['_display'])}
    
    # Selectbox avec autocomplétion
    selected_display = st.selectbox(
        "🔍 Sélectionner un membre",
        options=[""] + membre_options,
        format_func=lambda x: "Tapez pour rechercher..." if x == "" else x,
        key="membre_select"
    )
    
    # Afficher les informations du membre si un membre est sélectionné
    if 'selected_member' in st.session_state and st.session_state.selected_member is not None:
        row = df.loc[st.session_state.selected_member]
        nom = row[mapping["Nom"]]
        prenom = row[mapping["Prénom"]]
        statut = row[mapping["Statut de paiement"]]
        validation = row[mapping["Validation paiement bureau"]]
        montant = row[mapping["Montant dû"]]
        moyen = row[mapping["Moyen de paiement"]]
        
        # Afficher les informations du membre sélectionné
        st.markdown("### Informations du membre")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Nom complet", f"{nom.upper()} {prenom.capitalize()}")
        with col2:
            st.metric("Montant dû", f"{montant}€")
        with col3:
            status_icon = "✅" if str(statut).lower() == "payé" else "⏳"
            st.metric("Statut paiement", f"{status_icon} {statut}")
        with col4:
            valid_icon = "✅" if str(validation).lower() == "oui" else "❌"
            st.metric("Validation bureau", f"{valid_icon} {validation}")
        with col5:
            valid_icon = "❌" if pd.isna(moyen) else "✅"
            st.metric("Moyen de paiement", f"{valid_icon} {moyen}")
        
        st.info(f"**Moyen de paiement:** {moyen}")
    
    # Vérifier si la sélection a changé et est valide
    if selected_display and selected_display != "" and selected_display != st.session_state.previous_selection:
        st.session_state.selected_member = membre_dict[selected_display]
        # Mettre à jour l'état et passer à l'étape 4
        st.session_state.previous_selection = selected_display
        st.session_state.step = max(st.session_state.step, 4)
        st.rerun()