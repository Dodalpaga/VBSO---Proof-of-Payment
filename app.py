import streamlit as st
from utils.state import initialize_session_state
from utils.login_page import login_page
from utils.step1 import step1_upload_file
from utils.step2 import step2_map_columns
from utils.step3 import step3_search_member
from utils.step4 import step4_generate_invoice

# Configuration de la page
st.set_page_config(
    page_title="Gestion de Factures",
    page_icon="img/Logo VBSO white.png",  # Chemin vers le favicon
    layout="wide"
)
st.logo("img/Logo VBSO.png",
        icon_image="img/Logo VBSO.png",
        size="large")

def main_app():
    
    c1, c2 = st.columns(spec=[6,1], vertical_alignment="center")
    with c1:
        st.title("📄 Gestion de Factures Club | v1.0")
    with c2:
        # Logout button
        if st.button("🚪 Se déconnecter"):
            st.session_state.authenticated = False
            st.session_state.step = 1
            st.session_state.df = None
            st.session_state.columns_mapping = {}
            if 'selected_member' in st.session_state:
                del st.session_state.selected_member
            st.rerun()
    st.divider()

    # Création des onglets
    tab1, tab2, tab3 = st.tabs(["🏠 Accueil", "⚙️ Configuration", "✍️ Édition"])

    with tab1:
        st.header("Bienvenue dans l'application de gestion de factures")
        st.markdown("""
        Cette application permet de gérer les factures des membres d'un club en deux étapes simples :
        
        ### Ingestion :

        1. **Chargement du fichier** : Téléchargez et ingérez l'export excel de SportEasy contenant les informations des membres (nom, prénom, montant dû, etc.).
        """)
        
        st.image("img/tuto/export_sporteasy.png")
        
        st.markdown("""
        2. **Configuration des colonnes** : Associez les colonnes de votre fichier aux champs requis pour le traitement.
        """)
        
        st.image("img/tuto/validation_config.png")
        
        st.markdown("""
        Les éléments essentiels à l'édition de la facture sont les suivants :
        - Nom
        - Prénom
        - Montant dû
        - Validation du paiement par le bureau
        
        Les éléments suivants sont optionnels mais peuvent servir de contexte :
        - Moyen de paiement utilisé
        - Statut du paiement : C'est un indicateur créé par SportEasy au moement du paiement via la cagnotte.
        
        Les addresses de livraison et facturation seront à renseigner plus tard.
        
        ### Edition :
        
        1. **Recherche d'un membre** : Recherchez un membre spécifique pour vérifier ses informations de paiement.
        2. **Génération de la facture** : Saisissez les adresses et générez une facture au format Word pour le membre sélectionné.

        Cliquez sur l'onglet **Configuration** pour commencer !
        """)

    with tab2:
        # Étape 1 : Charger le fichier Excel
        if st.session_state.step >= 1:
            step1_upload_file()

        # Étape 2 : Mapper les colonnes
        if st.session_state.step >= 2 and st.session_state.df is not None:
            st.markdown("---")
            step2_map_columns()

    with tab3:
        if st.session_state.step<=2:
            st.info("Charger un extract de SportEasy et valider la cofiguration.")
        # Étape 3 : Rechercher un membre
        if st.session_state.step >= 3 and st.session_state.df is not None:
            step3_search_member()

        # Étape 4 : Saisir les adresses et générer la facture
        if st.session_state.step >= 4 and 'selected_member' in st.session_state:
            step4_generate_invoice()

# Initialiser l'état de la session
initialize_session_state()

# Afficher la page appropriée en fonction de l'état d'authentification
if not st.session_state.authenticated:
    login_page()
else:
    main_app()