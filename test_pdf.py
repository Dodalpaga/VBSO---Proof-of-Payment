from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Template PDF existant
template_path = "facture_template - empty.pdf"

# Lecture du template
reader = PdfReader(template_path)
writer = PdfWriter()

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)


can.setFont("Helvetica", 11)
can.setFillColor(colors.blue)
text = "Adresse de livraison\nLigne2\nLigne3"
y = 607
for line in text.splitlines():
    can.drawString(28, y, line)
    y -= 12   # move down for next line (line height)


can.setFont("Helvetica", 11)
can.setFillColor(colors.blue)
text = "Adresse de facturation\nLigne2\nLigne3"
y = 607
for line in text.splitlines():
    can.drawString(286, y, line)
    y -= 12   # move down for next line (line height)


can.setFont("Helvetica", 10)
can.setFillColor(colors.black)
can.drawRightString(480, 506, "8,50€")


can.setFont("Helvetica", 10)
can.setFillColor(colors.black)
can.drawRightString(564, 506, "8,50€")


can.setFont("Helvetica-Bold", 12)
can.setFillColor(colors.black)
can.drawRightString(564, 480, "8,50€")


can.setFont("Helvetica-Bold", 14)
can.setFillColor(colors.black)
can.drawRightString(564, 456, "8,50€")


can.setFont("Helvetica-Bold", 10)
can.setFillColor(colors.black)
can.drawRightString(70, 395, "8,50€")


can.setFont("Helvetica-Bold", 11)
can.setFillColor(colors.black)
can.drawRightString(160, 394, "15/10/2025")


can.setFont("Helvetica-Bold", 11)
can.setFillColor(colors.black)
can.drawRightString(568, 735, "15/10/2025")


can.setFont("Helvetica-Bold", 12)
can.setFillColor(colors.black)
can.drawRightString(568, 765, "15/10/2025")


can.setFont("Helvetica-Bold", 14)
can.setFillColor(colors.black)
can.drawRightString(568, 780, "N° FAC-042")


can.save()

packet.seek(0)
overlay_pdf = PdfReader(packet)

# Fusionner l'overlay avec le template
page = reader.pages[0]
page.merge_page(overlay_pdf.pages[0])
writer.add_page(page)

# Sauvegarder le résultat
with open("facture_final.pdf", "wb") as f:
    writer.write(f)
