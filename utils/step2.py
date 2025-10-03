import streamlit as st
from utils.toast_manager import add_persistent_toast

def step2_map_columns():
    
    st.header("2️⃣ Configuration des colonnes")
    
    # Si la configuration est déjà validée (step >= 3), afficher un résumé
    if st.session_state.step >= 3 and st.session_state.columns_mapping:
        st.success("✅ Configuration validée")
        
        # Afficher le mapping actuel
        with st.expander("📋 Voir la configuration actuelle"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Champ requis**")
                for field in st.session_state.columns_mapping.keys():
                    st.write(f"• {field}")
            with col2:
                st.markdown("**Colonne associée**")
                for column in st.session_state.columns_mapping.values():
                    st.write(f"→ {column}")
        
        # Option pour modifier la configuration
        if st.button("✏️ Modifier la configuration", type="secondary"):
            st.session_state.show_config = True
            st.rerun()
        
        # Si l'utilisateur veut modifier
        if 'show_config' not in st.session_state:
            st.session_state.show_config = False
            
        if not st.session_state.show_config:
            return  # Ne pas afficher le formulaire si pas en mode édition
    
    # Afficher le formulaire de configuration
    available_columns = list(st.session_state.df.columns)
    
    st.write("Associez les colonnes de votre fichier Excel aux champs requis:")
    
    col1, _, col3 = st.columns([30, 1, 10], vertical_alignment="center")
    
    with col1:
        st.dataframe(st.session_state.df)
    
    with col3:
        # Add empty option to allow no selection
        selectbox_options = [""] + available_columns
        
        # Helper function to get current index
        def get_index(field_name, column_name):
            current = st.session_state.columns_mapping.get(field_name, "")
            if current and current in available_columns:
                return selectbox_options.index(current)
            elif column_name in available_columns:
                return selectbox_options.index(column_name)
            return 0
        
        st.session_state.columns_mapping["Nom"] = st.selectbox(
            "Nom du membre",
            selectbox_options,
            index=get_index("Nom", "Nom"),
            key="col_nom"
        )
        if not st.session_state.columns_mapping["Nom"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Nom' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Prénom"] = st.selectbox(
            "Prénom du membre",
            selectbox_options,
            index=get_index("Prénom", "Prénom"),
            key="col_prenom"
        )
        if not st.session_state.columns_mapping["Prénom"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Prénom' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Moyen de paiement"] = st.selectbox(
            "Moyen de paiement utilisé",
            selectbox_options,
            index=get_index("Moyen de paiement", "Moyen de paiement"),
            key="col_paiement"
        )
        if not st.session_state.columns_mapping["Moyen de paiement"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Moyen de paiement' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Montant dû"] = st.selectbox(
            "Montant dû",
            selectbox_options,
            index=get_index("Montant dû", "Montant dû"),
            key="col_montant"
        )
        if not st.session_state.columns_mapping["Montant dû"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Montant dû' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Statut de paiement"] = st.selectbox(
            "Statut du paiement (Payé / Non payé)",
            selectbox_options,
            index=get_index("Statut de paiement", "Statut de paiement"),
            key="col_statut"
        )
        if not st.session_state.columns_mapping["Statut de paiement"]:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ Champ 'Statut de paiement' manquant</p>", unsafe_allow_html=True)
        
        st.session_state.columns_mapping["Validation paiement bureau"] = st.selectbox(
            "Validation paiement bureau (O /N)",
            selectbox_options,
            index=get_index("Validation paiement bureau", "Validation paiement bureau"),
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
            st.session_state.show_config = False  # Cacher le formulaire après validation
            add_persistent_toast(
                "Configuration validée ! Passez à l'onglet **Édition** pour rechercher un membre et générer une facture.",
                icon="✅"
            )
            st.rerun()