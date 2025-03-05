import os
from fpdf import FPDF

OUTPUT_DIR = "generated_forms"

def generate_pdf(form_data: dict, filename: str = "registration_form.pdf"):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_path = os.path.join(OUTPUT_DIR, filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    pdf.cell(0, 10, "Patient Registration Form", ln=True, align="C")
    pdf.ln(10)

    for key, value in form_data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    pdf.output(file_path)
    return file_path
