import streamlit as st
import pandas as pd
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat
from docxtpl import DocxTemplate
import re
from io import BytesIO

# Configuration de la page
st.set_page_config(page_title="Gestion de Factures", page_icon="📄", layout="wide")

def pretty_format_phone(number, default_region="FR"):
    if pd.isna(number):
        return None
    num_str = str(number).replace(".0", "").strip()
    try:
        parsed = phonenumbers.parse(num_str, default_region)
    except phonenumbers.NumberParseException:
        return num_str
    intl = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
    intl = intl.replace("+", "(+")
    intl = intl.replace(" ", ") ", 1)
    intl = intl.replace(" ", ".")
    return intl

def clean_filename(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\d_-]", "_", s)
    return s

# Initialisation de la session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'columns_mapping' not in st.session_state:
    st.session_state.columns_mapping = {}
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("📄 Gestion de Factures Club | v1.0")
st.markdown("---")

# ÉTAPE 1: Charger le fichier Excel
if st.session_state.step >= 1:
    st.header("1️⃣ Charger le fichier des membres")
    
    uploaded_file = st.file_uploader("Sélectionnez le fichier Excel des membres", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success(f"✅ Fichier chargé avec succès! {len(df)} membres trouvés.")
            st.session_state.step = max(st.session_state.step, 2)
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {e}")

# ÉTAPE 2: Mapper les colonnes
if st.session_state.step >= 2 and st.session_state.df is not None:
    st.markdown("---")
    st.header("2️⃣ Configuration des colonnes")
    
    df = st.session_state.df
    available_columns = list(df.columns)
    
    required_fields = {
        "Nom": "Nom",
        "Prénom": "Prénom",
        "Moyen de paiement": "Moyen de paiement",
        "Montant dû": "Montant dû",
        "Statut de paiement": "Statut de paiement",
        "Validation paiement bureau": "Validation paiement bureau"
    }
    
    st.write("Associez les colonnes de votre fichier Excel aux champs requis:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.session_state.columns_mapping["Nom"] = st.selectbox(
            "Colonne Nom",
            available_columns,
            index=available_columns.index("Nom") if "Nom" in available_columns else 0,
            key="col_nom"
        )
        st.session_state.columns_mapping["Prénom"] = st.selectbox(
            "Colonne Prénom",
            available_columns,
            index=available_columns.index("Prénom") if "Prénom" in available_columns else 0,
            key="col_prenom"
        )
    
    with col2:
        st.session_state.columns_mapping["Moyen de paiement"] = st.selectbox(
            "Colonne Moyen de paiement",
            available_columns,
            index=available_columns.index("Moyen de paiement") if "Moyen de paiement" in available_columns else 0,
            key="col_paiement"
        )
        st.session_state.columns_mapping["Montant dû"] = st.selectbox(
            "Colonne Montant dû",
            available_columns,
            index=available_columns.index("Montant dû") if "Montant dû" in available_columns else 0,
            key="col_montant"
        )
    
    with col3:
        st.session_state.columns_mapping["Statut de paiement"] = st.selectbox(
            "Colonne Statut de paiement",
            available_columns,
            index=available_columns.index("Statut de paiement") if "Statut de paiement" in available_columns else 0,
            key="col_statut"
        )
        st.session_state.columns_mapping["Validation paiement bureau"] = st.selectbox(
            "Colonne Validation paiement bureau",
            available_columns,
            index=available_columns.index("Validation paiement bureau") if "Validation paiement bureau" in available_columns else 0,
            key="col_validation"
        )
    
    if st.button("✅ Valider la configuration", type="primary"):
        st.session_state.step = max(st.session_state.step, 3)
        st.rerun()

# ÉTAPE 3: Rechercher un membre
if st.session_state.step >= 3 and st.session_state.df is not None:
    st.markdown("---")
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
    
    if selected_display and selected_display != "":
        idx = membre_dict[selected_display]
        row = df.loc[idx]
        
        nom = row[mapping["Nom"]]
        prenom = row[mapping["Prénom"]]
        statut = row[mapping["Statut de paiement"]]
        validation = row[mapping["Validation paiement bureau"]]
        montant = row[mapping["Montant dû"]]
        moyen = row[mapping["Moyen de paiement"]]
        
        # Afficher les informations du membre sélectionné
        st.markdown("### Informations du membre")
        col1, col2, col3, col4 = st.columns(4)
        
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
        
        st.info(f"**Moyen de paiement:** {moyen}")
        
        if st.button("➡️ Continuer avec ce membre", type="primary", use_container_width=True):
            st.session_state.selected_member = idx
            st.session_state.step = max(st.session_state.step, 4)
            st.rerun()

# ÉTAPE 4: Saisir les adresses et générer la facture
if st.session_state.step >= 4 and 'selected_member' in st.session_state:
    st.markdown("---")
    st.header("4️⃣ Génération de la facture")
    
    df = st.session_state.df
    mapping = st.session_state.columns_mapping
    membre = df.loc[st.session_state.selected_member]
    
    nom = membre[mapping["Nom"]]
    prenom = membre[mapping["Prénom"]]
    statut = str(membre[mapping["Statut de paiement"]]).lower()
    validation = str(membre[mapping["Validation paiement bureau"]]).lower()
    
    st.subheader(f"Membre sélectionné: {nom.upper()} {prenom.capitalize()}")
    
    # Vérifier les conditions
    if statut != "payé":
        st.error("❌ La facture ne peut pas être générée: le paiement n'a pas été effectué.")
        if st.button("← Retour à la recherche"):
            st.session_state.step = 3
            del st.session_state.selected_member
            st.rerun()
        st.stop()
    
    if validation != "oui":
        st.error("❌ La facture ne peut pas être générée: la validation par le bureau n'a pas été effectuée.")
        if st.button("← Retour à la recherche"):
            st.session_state.step = 3
            del st.session_state.selected_member
            st.rerun()
        st.stop()
    
    st.success("✅ Paiement effectué et validé par le bureau")
    
    # Formulaire d'adresses
    st.subheader("Adresses")
    
    col1, col2, col3 = st.columns([5, 1, 5])
    
    with col1:
        adresse_livraison = st.text_area(
            "Adresse de livraison", 
            height=150, 
            key="addr_livraison", 
            placeholder="Numéro et rue\nCode postal et ville\nPays",
            label_visibility="visible"
        )
    
    with col2:
        st.write("")
        st.write("")
        same_address = st.checkbox("Identique", value=True, key="same_addr")
    
    with col3:
        if same_address:
            st.text_area(
                "Adresse de facturation", 
                height=150, 
                value=adresse_livraison, 
                disabled=True, 
                key="addr_fact_display",
                label_visibility="visible"
            )
            adresse_facturation = adresse_livraison
        else:
            adresse_facturation = st.text_area(
                "Adresse de facturation", 
                height=150, 
                key="addr_facturation",
                placeholder="Numéro et rue\nCode postal et ville\nPays",
                label_visibility="visible"
            )
    
    # Vérifier si le template existe
    import os
    template_path = "facture_template.docx"
    template_exists = os.path.exists(template_path)
    
    if not template_exists:
        st.error("❌ Le fichier template 'facture_template.docx' est introuvable dans le même dossier que l'application.")
        st.info("💡 Assurez-vous que le fichier 'facture_template.docx' se trouve dans le même répertoire que app.py")
        st.stop()
    
    if st.button("🎉 Générer la facture", type="primary", use_container_width=True):
        if not adresse_livraison:
            st.toast("❌ Veuillez renseigner une adresse de livraison")
            st.stop()
        try:
            # Charger le template depuis le fichier local
            doc = DocxTemplate(template_path)
            
            # Préparer le contexte
            contexte = {
                "nom": nom,
                "prenom": prenom,
                "montant_du": membre[mapping["Montant dû"]],
                "moyen_paiement": membre[mapping["Moyen de paiement"]],
                "statut_paiement": membre[mapping["Statut de paiement"]],
                "validation": membre[mapping["Validation paiement bureau"]],
                "adresse_facturation": adresse_facturation,
                "adresse_livraison": adresse_livraison,
            }
            
            # Générer le document
            doc.render(contexte)
            
            # Sauvegarder dans un buffer
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            # Proposer le téléchargement
            filename = f"facture_{clean_filename(nom)}_{clean_filename(prenom)}.docx"
            
            st.success("✅ Facture générée avec succès!")
            st.download_button(
                label="📥 Télécharger la facture",
                data=buffer,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération de la facture: {e}")
    
    if st.button("← Retour à la recherche"):
        st.session_state.step = 3
        del st.session_state.selected_member
        st.rerun()
