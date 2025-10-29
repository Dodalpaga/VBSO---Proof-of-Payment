from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def generer_facture_pdf(template_path, donnees):
    """
    Génère une facture au format PDF à partir d'un template.
    
    Args:
        template_path (str): Chemin vers le fichier template .pdf
        donnees (dict): Dictionnaire contenant les données de la facture
            - nom (str): Nom du membre
            - prenom (str): Prénom du membre
            - nom_payant (str): Nom du payant
            - prenom_payant (str): Prénom du payant
            - produit (str): Produit acheté (type de licence avec ou sans assurance)
            - date_jour (str): Date du jour au format JJ/MM/AAAA
            - montant_du (float/str): Montant dû
            - adresse_facturation (str): Adresse de facturation
            - adresse_livraison (str): Adresse de livraison
    
    Returns:
        BytesIO: Buffer contenant le document PDF généré
    
    Raises:
        Exception: En cas d'erreur lors de la génération
    """
    
    try:
        # Lecture du template
        reader = PdfReader(template_path)
        writer = PdfWriter()
        
        # Créer un overlay avec les données
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Formatage du montant
        montant_str = f"{donnees['montant_du']}"
        if not montant_str.endswith('€'):
            montant_str = f"{montant_str}€"
        
        # === ADRESSE DE LIVRAISON ===
        can.setFont("Helvetica", 11)
        can.setFillColor(colors.black)
        y = 607
        can.drawString(28, y, f"{donnees['prenom']} {donnees['nom']}")
        for line in donnees["adresse_livraison"].splitlines():
            y -= 12
            can.drawString(28, y, line)
        
        # === ADRESSE DE FACTURATION ===
        can.setFont("Helvetica", 11)
        can.setFillColor(colors.black)
        y = 607
        can.drawString(286, y, f"{donnees['prenom']} {donnees['nom']}")
        for line in donnees["adresse_facturation"].splitlines():
            y -= 12
            can.drawString(286, y, line)
        
        # === MONTANTS (toutes les occurrences) ===
        # Montant unitaire HT
        can.setFont("Helvetica", 10)
        can.setFillColor(colors.black)
        can.drawRightString(480, 506, montant_str)
        
        # Montant total HT
        can.setFont("Helvetica", 10)
        can.setFillColor(colors.black)
        can.drawRightString(564, 506, montant_str)
        
        # Total HT (en gras)
        can.setFont("Helvetica-Bold", 12)
        can.setFillColor(colors.black)
        can.drawRightString(564, 480, montant_str)
        
        # Total TTC (en gras, plus gros)
        can.setFont("Helvetica-Bold", 14)
        can.setFillColor(colors.black)
        can.drawRightString(564, 456, montant_str)
        
        # Montant payé
        can.setFont("Helvetica-Bold", 10)
        can.setFillColor(colors.black)
        can.drawRightString(70, 395, montant_str)
        
        # Beneficiaire
        can.setFont("Helvetica-Bold", 10)
        can.setFillColor(colors.black)
        can.drawRightString(260, 394, f"{donnees['nom']} {donnees['prenom']}")
        
        # === DATES ===
        date_str = donnees["date_jour"]
        
        # Date de paiement
        can.setFont("Helvetica-Bold", 11)
        can.setFillColor(colors.black)
        can.drawRightString(155, 394, date_str)
        
        # Date d'émission (coin droit)
        can.setFont("Helvetica-Bold", 11)
        can.setFillColor(colors.black)
        can.drawRightString(568, 735, date_str)

        # === NUMÉRO DE FACTURE ===
        numero_facture = donnees["n_facture"]
        
        can.setFont("Helvetica-Bold", 16)
        can.setFillColor(colors.black)
        can.drawRightString(568, 772, numero_facture)
        
        # Finaliser le canvas
        can.save()
        
        # Fusionner l'overlay avec le template
        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        
        page = reader.pages[0]
        page.merge_page(overlay_pdf.pages[0])
        writer.add_page(page)
        
        # Sauvegarder le résultat dans un buffer
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer
        
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du document PDF: {str(e)}")