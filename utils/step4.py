import streamlit as st
import os
from docxtpl import DocxTemplate
from io import BytesIO
import re

def step4_generate_invoice():
    
    def clean_filename(s):
        s = s.lower().strip()
        s = re.sub(r"[^\w\d_-]", "_", s)
        return s
    
    st.header("4️⃣ Génération de la facture")
    
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
            "La facture ne peut pas être générée: le paiement n'a pas été effectué.",
            icon="❌",
            duration="long"
        )
        if st.button("← Retour à la recherche"):
            st.session_state.step = 3
            del st.session_state.selected_member
            st.rerun()
        st.stop()
    
    if validation != "oui":
        st.toast(
            "La facture ne peut pas être générée: la validation par le bureau n'a pas été effectuée.",
            icon="❌",
            duration="long"
        )
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
    
    # Vérifier si le template existe
    template_path = "facture_template.docx"
    template_exists = os.path.exists(template_path)
    
    if not template_exists:
        st.toast(
            "Le fichier template 'facture_template.docx' est introuvable dans le même dossier que l'application.",
            icon="❌",
            duration="long"
        )
        st.info("💡 Assurez-vous que le fichier 'facture_template.docx' se trouve dans le même répertoire que app.py")
        st.stop()
        
    _, col, _ = st.columns([3,1,3])
    
    with col:
    
        if st.button("🎉 Générer la facture", type="primary", use_container_width=True):
            if not (adresse_livraison and adresse_facturation):
                st.toast(
                    "Erreur : Veuillez renseigner une adresse de livraison et une adresse de facturation.",
                    icon="❌",
                    duration="long"
                )
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
                
                st.toast(
                    "Facture générée avec succès!",
                    icon="✅",
                    duration="long"
                )
                st.download_button(
                    label="📥 Télécharger la facture",
                    data=buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=False
                )
                
            except Exception as e:
                st.toast(
                    f"Erreur lors de la génération de la facture: {e}",
                    icon="❌",
                    duration="long"
                )
    
    if st.button("← Retour à la recherche"):
        st.session_state.step = 3
        del st.session_state.selected_member
        st.rerun()