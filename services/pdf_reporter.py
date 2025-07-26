from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(gpt_text, filename="match_report.pdf"):
    path = os.path.join("assets", filename)
    os.makedirs("assets", exist_ok=True)

    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    lines = gpt_text.strip().split("\n")
    y = height - 40

    for line in lines:
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line.strip())
        y -= 16

    c.save()
    return path