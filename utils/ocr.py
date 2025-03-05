from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    text = ""

    # OCR each page
    for page_num, page in enumerate(pages, start=1):
        temp_image = f"temp_page_{page_num}.png"
        page.save(temp_image, "PNG")

        text += pytesseract.image_to_string(Image.open(temp_image))
        text += "\n"

        os.remove(temp_image)

    return text

def extract_text(file_path: str) -> str:
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type. Only images and PDFs are supported.")
