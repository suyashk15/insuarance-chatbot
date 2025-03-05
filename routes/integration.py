from fastapi import APIRouter
from services.form_generator import generate_pdf

router = APIRouter()

@router.post("/generate-form/")
async def generate_form(data: dict):
    filename = generate_pdf(data)
    return {"filename": filename}

@router.post("/submit-form/")
async def submit_form(data: dict):
    # Mock API call to hospital system
    return {"status": "Success", "message": "Form submitted to hospital system"}
