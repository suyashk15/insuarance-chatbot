from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from models.document import Document, SessionLocal
from utils.ocr import extract_text
from utils.openai_client import generate_response
import json

import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        extracted_text = extract_text(file_location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    organized_data = await generate_response(f"Extract and return JSON-formatted insurance details: {extracted_text}")

    organized_data_json = json.dumps(organized_data)

    async with SessionLocal() as session:
        new_doc = Document(filename=file.filename, extracted_data=organized_data_json)
        session.add(new_doc)
        await session.commit()

    return {"filename": file.filename, "data": organized_data}

@router.get("/documents/{doc_id}")
async def get_document(doc_id: int):
    async with SessionLocal() as session:
        doc = await session.get(Document, doc_id)
        if not doc:
            return JSONResponse(content={"error": "Document not found"}, status_code=404)

        extracted_data_dict = json.loads(doc.extracted_data)

        return {"filename": doc.filename, "data": extracted_data_dict}

