import streamlit as st

def step2_map_columns():
    
    st.header("2️⃣ Configuration des colonnes")
    
    available_columns = list(st.session_state.df.columns)
    
    st.write("Associez les colonnes de votre fichier Excel aux champs requis:")
    
    col1, _, col3 = st.columns([30,1,10], vertical_alignment="center")
    
    with col1:
        st.dataframe(st.session_state.df)
    
    with col3:
        # Add empty option to allow no selection
        selectbox_options = [""] + available_columns
        
        st.session_state.columns_mapping["Nom"] = st.selectbox(
            "Nom du membre",
            selectbox_options,
            index=selectbox_options.index("Nom") if "Nom" in available_columns else 0,
            key="col_nom"
        )
        if not st.session_state.columns_mapping["Nom"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Nom' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Prénom"] = st.selectbox(
            "Prénom du membre",
            selectbox_options,
            index=selectbox_options.index("Prénom") if "Prénom" in available_columns else 0,
            key="col_prenom"
        )
        if not st.session_state.columns_mapping["Prénom"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Prénom' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Moyen de paiement"] = st.selectbox(
            "Moyen de paiement utilisé",
            selectbox_options,
            index=selectbox_options.index("Moyen de paiement") if "Moyen de paiement" in available_columns else 0,
            key="col_paiement"
        )
        if not st.session_state.columns_mapping["Moyen de paiement"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Moyen de paiement' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Montant dû"] = st.selectbox(
            "Montant dû",
            selectbox_options,
            index=selectbox_options.index("Montant dû") if "Montant dû" in available_columns else 0,
            key="col_montant"
        )
        if not st.session_state.columns_mapping["Montant dû"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Montant dû' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Statut de paiement"] = st.selectbox(
            "Statut du paiement (Payé / Non payé)",
            selectbox_options,
            index=selectbox_options.index("Statut de paiement") if "Statut de paiement" in available_columns else 0,
            key="col_statut"
        )
        if not st.session_state.columns_mapping["Statut de paiement"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Statut de paiement' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Validation paiement bureau"] = st.selectbox(
            "Validation paiement bureau (O /N)",
            selectbox_options,
            index=selectbox_options.index("Validation paiement bureau") if "Validation paiement bureau" in available_columns else 0,
            key="col_validation"
        )
        if not st.session_state.columns_mapping["Validation paiement bureau"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Validation paiement bureau' manquant</p>", unsafe_allow_html=True)

    # Validation and button logic
    required_fields = ["Nom", "Prénom", "Moyen de paiement", "Montant dû", "Statut de paiement", "Validation paiement bureau"]
    missing_fields = [field for field in required_fields if not st.session_state.columns_mapping.get(field)]

    if missing_fields:
        st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Veuillez sélectionner tous les champs requis avant de valider.</p>", unsafe_allow_html=True)
        st.button("✅ Valider la configuration", type="primary", disabled=True)
    else:
        if st.button("✅ Valider la configuration", type="primary"):
            st.session_state.step = 3
            st.toast(
                "Configuration validée ! Passez à l'onglet **Édition** pour rechercher un membre et générer une facture.",
                icon="✅",
                duration="long"
            )
            st.rerun()
