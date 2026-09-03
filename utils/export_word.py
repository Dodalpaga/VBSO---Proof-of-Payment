from docxtpl import DocxTemplate
from io import BytesIO
from datetime import datetime

def generer_facture_word(template_path, donnees):
    """
    Génère une facture au format Word (.docx) à partir d'un template.
    
    Args:
        template_path (str): Chemin vers le fichier template .docx
        donnees (dict): Dictionnaire contenant les données de la facture
            - nom (str): Nom du membre
            - prenom (str): Prénom du membre
            - nom_payant (str): Nom du payant
            - prenom_payant (str): Prénom du payant
            - produit (str): Produit acheté (type de licence avec ou sans assurance)
            - date_jour (str): Date du jour au format JJ/MM/AAAA
            - montant_du (float/str): Montant dû
            - moyen_paiement (str): Moyen de paiement utilisé
            - statut_paiement (str): Statut du paiement
            - validation (str): Validation du bureau
            - adresse_facturation (str): Adresse de facturation
            - adresse_livraison (str): Adresse de livraison
    
    Returns:
        BytesIO: Buffer contenant le document Word généré
    
    Raises:
        Exception: En cas d'erreur lors de la génération
    """
    
    try:
        # Charger le template
        doc = DocxTemplate(template_path)
        
        # Préparer le contexte pour le template
        contexte = {
            "nom": donnees["nom"],
            "prenom": donnees["prenom"],
            "nom_payant": donnees["nom_payant"],
            "prenom_payant": donnees["prenom_payant"],
            "produit": donnees["produit"],
            "date_jour": donnees["date_jour"],
            "montant_du": donnees["montant_du"],
            "moyen_paiement": donnees["moyen_paiement"],
            "statut_paiement": donnees["statut_paiement"],
            "validation": donnees["validation"],
            "adresse_facturation": donnees["adresse_facturation"],
            "adresse_livraison": donnees["adresse_livraison"],
            "n_facture": donnees["n_facture"]
        }
        
        # Générer le document
        doc.render(contexte)
        
        # Sauvegarder dans un buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du document Word: {str(e)}")