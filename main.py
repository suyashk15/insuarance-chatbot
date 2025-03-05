from fastapi import FastAPI
from routes import chatbot, document
from models.document import init_db as init_document_db
from models.conversation import init_db as init_conversation_db
from routes import integration

app = FastAPI()

app.include_router(integration.router, prefix="/integration", tags=["Integration"])
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

@app.on_event("startup")
async def on_startup():
    await init_document_db()
    await init_conversation_db()

@app.get("/")
async def read_root():
    return {"message": "Insurance Chatbot API is running"}