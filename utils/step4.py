import streamlit as st
import os
import re
import base64
from datetime import datetime
from utils.export_word import generer_facture_word
from utils.export_pdf import generer_facture_pdf

def step4_generate_invoice():
    
    def clean_filename(s):
        s = s.lower().strip()
        s = re.sub(r"[^\w\d_-]", "_", s)
        return s
    
    st.header("4️⃣ Génération de la facture")
    
    if st.session_state.selected_member is not None:
    
        df = st.session_state.df
        mapping = st.session_state.columns_mapping
        membre = df.loc[st.session_state.selected_member]
        
        nom = membre[mapping["Nom"]]
        prenom = membre[mapping["Prénom"]]
        statut = str(membre[mapping["Statut de paiement"]]).lower()
        validation = str(membre[mapping["Validation paiement bureau"]]).lower()
        
        st.markdown(f"<h3>Membre sélectionné: <div style='color: #FF584D;'>{nom.upper()} {prenom.capitalize()}</div></h3>", unsafe_allow_html=True)
        
        st.dataframe(membre.dropna().drop(["_search","_display"]))
        
        # Vérifier les conditions
        if statut != "payé":
            st.toast(
                f"La facture ne peut pas être générée car {prenom} {nom} n'a pas effectué son paiement",
                icon="❌",
                duration="long"
            )
            st.stop()
        
        if validation != "oui":
            st.toast(
                f"La facture ne peut pas être générée car la validation du paiement de {prenom} {nom} n'a pas encore été faite par le Bureau",
                icon="❌",
                duration="long"
            )
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
            same_address = st.checkbox("Addresse de facturation identique", value=True, key="same_addr")
        
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
        
        # Choix du format d'export
        st.subheader("Format de la facture")
        format_export = st.radio(
            "Choisissez le format d'export :",
            options=["PDF (.pdf)", "Word (.docx)"],
            horizontal=True,
            key="format_export"
        )
        
        # Vérifier si le template existe
        if format_export == "Word (.docx)":
            template_path = "templates/facture_template.docx"
        else:
            template_path = "templates/facture_template - empty.pdf"
            
        template_exists = os.path.exists(template_path)
        
        if not template_exists:
            st.toast(
                f"Le fichier template '{template_path}' est introuvable dans le même dossier que l'application.",
                icon="❌",
                duration="long"
            )
            st.info(f"💡 Assurez-vous que le fichier '{template_path}' se trouve dans le même répertoire que app.py")
            st.stop()
            
        # Bouton unique de génération et téléchargement
        _, col, _ = st.columns([3, 1, 3])
        
        with col:
            if st.button(
                "Générer la facture",
                icon="🎉",
                type="primary",
                use_container_width=True,
                key="generation_button"
            ):
                # Vérifier si les adresses sont remplies
                if not (adresse_livraison and adresse_facturation):
                    # Afficher un message d'erreur si les adresses manquent
                    st.error("⚠️ Veuillez renseigner les deux adresses avant de générer la facture")
                else:
                    # Préparer les données
                    donnees_facture = {
                        "nom": nom,
                        "prenom": prenom,
                        "date_jour": datetime.today().strftime("%d/%m/%Y"),
                        "montant_du": membre[mapping["Montant dû"]],
                        "moyen_paiement": membre[mapping["Moyen de paiement"]],
                        "statut_paiement": membre[mapping["Statut de paiement"]],
                        "validation": membre[mapping["Validation paiement bureau"]],
                        "adresse_facturation": adresse_facturation,
                        "adresse_livraison": adresse_livraison,
                        # Générer un numéro de facture basé sur le nom/prénom/date
                        "n_facture":f"N° FAC-{datetime.strptime(datetime.today().strftime('%d/%m/%Y'), '%d/%m/%Y').strftime('%y%m')}-{nom[:3].upper()}{prenom[:2].upper()}"
                    }
                    
                    try:
                        # Générer selon le format choisi
                        if format_export == "Word (.docx)":
                            buffer = generer_facture_word(template_path, donnees_facture)
                            extension = "docx"
                            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        else:
                            buffer = generer_facture_pdf(template_path, donnees_facture)
                            extension = "pdf"
                            mime_type = "application/pdf"
                        
                        filename = f"facture_{clean_filename(nom)}_{clean_filename(prenom)}.{extension}"
                        
                        # Téléchargement direct
                        st.download_button(
                            label="Télécharger la facture",
                            icon="⬇️",
                            data=buffer,
                            file_name=filename,
                            mime=mime_type,
                            type="primary",
                            use_container_width=True,
                            key="download_button"  # Unique key to avoid conflicts
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération: {str(e)}")