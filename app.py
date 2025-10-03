import streamlit as st
from utils.state import initialize_session_state
from utils.login_page import login_page
from utils.step1 import step1_upload_file
from utils.step2 import step2_map_columns
from utils.step3 import step3_search_member
from utils.step4 import step4_generate_invoice
from utils.toast_manager import display_pending_toasts

# Configuration de la page
st.set_page_config(
    page_title="Gestion de Factures",
    page_icon="img/Logo VBSO white.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.logo("img/Logo VBSO.png",
        icon_image="img/Logo VBSO.png",
        size="large")

def sidebar_navigation():
    """Gère la navigation dans la sidebar"""
    with st.sidebar:
        st.title("📄 Gestion de Factures")
        st.caption("© VBSO | v1.0")
        
        # Boutons de téléchargement
        st.subheader("📥 Téléchargements")
        
        # Charger le fichier PDF
        with open("templates/facture_formulaire_vierge.pdf", "rb") as f:
            pdf_bytes = f.read()

        # Charger le fichier Word
        with open("templates/facture_template.docx", "rb") as f:
            docx_bytes = f.read()
        
        # Bouton pour télécharger le PDF
        st.download_button(
            label="📝 Formulaire vierge PDF",
            data=pdf_bytes,
            file_name="facture_vierge.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_pdf"
        )

        # Bouton pour télécharger le Word
        st.download_button(
            label="📝 Formulaire vierge WORD",
            data=docx_bytes,
            file_name="facture_vierge.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            key="download_word"
        )
        
        # Navigation par pages
        st.subheader("📑 Navigation")
        
        # Initialiser la page si elle n'existe pas
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Accueil"
        
        # Boutons de navigation
        if st.button("🏠 Accueil", use_container_width=True, 
                     type="primary" if st.session_state.current_page == "Accueil" else "secondary"):
            st.session_state.current_page = "Accueil"
            st.rerun()
        
        if st.button("⚙️ Configuration", use_container_width=True,
                     type="primary" if st.session_state.current_page == "Configuration" else "secondary"):
            st.session_state.current_page = "Configuration"
            st.rerun()
        
        # Désactiver le bouton Édition si la configuration n'est pas complète
        edition_disabled = st.session_state.step <= 2
        if st.button("✍️ Édition", use_container_width=True, 
                     disabled=edition_disabled,
                     type="primary" if st.session_state.current_page == "Édition" else "secondary"):
            st.session_state.current_page = "Édition"
            st.rerun()
        
        if edition_disabled:
            st.caption("⚠️ Complétez la configuration pour accéder à l'édition")
        
        st.divider()
        
        # Bouton de déconnexion
        if st.button("🚪 Se déconnecter", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.step = 1
            st.session_state.df = None
            st.session_state.columns_mapping = {}
            st.session_state.current_page = "Accueil"
            if 'selected_member' in st.session_state:
                del st.session_state.selected_member
            st.rerun()

def page_accueil():
    """Page d'accueil"""
    st.title("🏠 Accueil")
    st.header("Bienvenue dans l'application de gestion de factures")
    st.markdown("""
    Cette application permet de gérer les factures des membres d'un club en deux étapes simples :
    
    ### Ingestion :

    1. **Chargement du fichier** : Téléchargez et ingérez l'export excel de SportEasy contenant les informations des membres (nom, prénom, montant dû, etc.).
    """)
    
    st.image("img/tuto/export_sporteasy.png", width=1000)
    
    st.markdown("""
    2. **Configuration des colonnes** : Associez les colonnes de votre fichier aux champs requis pour le traitement.
    """)
    
    st.image("img/tuto/validation_config.png", width=1000)
    
    st.markdown("""
    Les éléments essentiels à l'édition de la facture sont les suivants :
    - Nom
    - Prénom
    - Montant dû
    - Validation du paiement par le bureau
    
    Les éléments suivants sont optionnels mais peuvent servir de contexte :
    - Moyen de paiement utilisé
    - Statut du paiement : C'est un indicateur créé par SportEasy au moment du paiement via la cagnotte.
    
    Les adresses de livraison et facturation seront à renseigner plus tard.
    
    ### Edition :
    
    1. **Recherche d'un membre** : Recherchez un membre spécifique pour vérifier ses informations de paiement.
    2. **Génération de la facture** : Saisissez les adresses et générez une facture au format Word pour le membre sélectionné.

    Cliquez sur **Configuration** dans la sidebar pour commencer !
    """)

def page_configuration():
    """Page de configuration"""
    st.title("⚙️ Configuration")
    
    # Étape 1 : Charger le fichier Excel
    if st.session_state.step >= 1:
        step1_upload_file()

    # Étape 2 : Mapper les colonnes
    if st.session_state.step >= 2 and st.session_state.df is not None:
        st.markdown("---")
        step2_map_columns()

def page_edition():
    """Page d'édition"""
    st.title("✍️ Édition")
    
    if st.session_state.step <= 2:
        st.info("Charger un extract de SportEasy et valider la configuration.")
        return
    
    # Étape 3 : Rechercher un membre
    if st.session_state.step >= 3 and st.session_state.df is not None:
        step3_search_member()

    # Étape 4 : Saisir les adresses et générer la facture
    if st.session_state.step >= 4 and 'selected_member' in st.session_state:
        step4_generate_invoice()

def main_app():
    """Application principale"""
    # IMPORTANT : Afficher les toasts en attente AVANT tout le reste
    display_pending_toasts()
    
    # Navigation dans la sidebar
    sidebar_navigation()
    
    # Afficher la page appropriée
    if st.session_state.current_page == "Accueil":
        page_accueil()
    elif st.session_state.current_page == "Configuration":
        page_configuration()
    elif st.session_state.current_page == "Édition":
        page_edition()

# Initialiser l'état de la session
initialize_session_state()

# Afficher la page appropriée en fonction de l'état d'authentification
if not st.session_state.authenticated:
    login_page()
else:
    main_app()