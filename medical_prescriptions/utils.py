from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(prescription_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Doctor ID: {prescription_data['doctor_id']}")
    p.drawString(100, height - 120, f"Patient ID: {prescription_data['patient_id']}")
    p.drawString(100, height - 140, f"Medication ID: {prescription_data['medication_ids']}")
    p.drawString(100, height - 160, f"Description: {prescription_data['description']}")
    p.drawString(100, height - 180, f"Dose: {prescription_data['dose']}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()
