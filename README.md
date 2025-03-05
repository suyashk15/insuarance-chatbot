# 🏥 AI-Powered Insurance Chatbot

This project is an **AI-powered conversational assistant** for **insurance document processing** and **form completion** using **FastAPI**, **GPT-4o**, **Tesseract OCR**, and **Streamlit**.

🚀 **Key Features**
- 📂 **Upload Insurance Documents** (PDFs/Images)
- 🔍 **Extract Insurance Details** using **OCR**
- 🤖 **Chatbot** for **validating & confirming missing details**
- 📑 **Generate Registration Forms** (PDF format)
- 📢 **Answer General Insurance Queries**

---

## **🛠 Tech Stack**
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o
- **OCR**: Tesseract OCR
- **Database**: SQLite with SQLAlchemy

---

## **📌 Installation Guide**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/suyashk15/insurance-chatbot.git
cd insurance-chatbot
```

### 2️⃣ Set Up a Virtual Environment 
```bash
python -m venv .venv
cd .venv\Scripts\     # Windows
activate
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Set Up Environment Variables
- Create a .env file in the project root and add:
```bash
OPENAI_API_KEY=
```
- Place your credentials from OpenAI.

### 5️⃣ Install Tesseract OCR and Poppler
- Windows: Download & Install Tesseract and Poppler add the path to your system variables.
- Place appropriate paths for both in utils\ocr.py

### 6️⃣ Start the FastAPI Backend
```bash
uvicorn main:app --reload
```
- The API server will run at http://127.0.0.1:8000
- Open http://127.0.0.1:8000/docs for interactive API documentation.

### 🚀 **Running the Streamlit Frontend**
```bash
streamlit run streamlit_app.py
```
- This starts the web UI which user can interact with

---

## 📌 How It Works

### 1️⃣ Upload an Insurance Document

- **Upload a PDF or Image (JPG/PNG)** containing **insurance details**.
- **OCR extracts text** from the document.
- **GPT-4o organizes the details into structured JSON.**

### 2️⃣ View Extracted Insurance Details

- Extracted details **are displayed in tables** (instead of raw JSON).
- Includes:
  - **Policy Holder Information**
  - **Policy Details**
  - **Coverage Information**
  - **Exclusions & Limitations**

### 3️⃣ Chat with the Insurance Assistant

- **Validate & Confirm Missing Details**
  - The chatbot asks for any missing details.
  - User provides responses, and the chatbot updates the form.
- **General Insurance Queries**
  - Ask about **coverage details, deductibles, and policy terms**.
  - The chatbot responds using GPT-4o.

### 4️⃣ Generate & Download Registration Form

- Once details are confirmed, a **PDF registration form is generated**.
- The completed form is **ready for submission to the hospital system**.

---

## 📌 API Endpoints

### 📂 Document Upload & Processing

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| `POST` | `/documents/upload/`  | Upload a document for extraction |
| `GET`  | `/documents/{doc_id}` | Retrieve extracted details       |

### 🤖 Chatbot

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| `POST` | `/chatbot/chat/` | Chat with the AI assistant |

### 📑 Form Generation

| Method | Endpoint                      | Description                      |
| ------ | ----------------------------- | -------------------------------- |
| `POST` | `/integration/generate-form/` | Generate a PDF registration form |

---
## 📌 High-Level Design Document

### **1️⃣ Overview of System Architecture**
The AI-Powered Insurance Chatbot is designed to automate **insurance document processing**, **form completion**, and **conversational validation** using a combination of **FastAPI, GPT-4o, Tesseract OCR, SQLite, and Streamlit**.

### **🔹 Key System Components**
1. **FastAPI Backend** - Handles document processing, AI-powered conversation, and form generation.
2. **Tesseract OCR** - Extracts text from uploaded PDFs and images.
3. **OpenAI GPT-4o** - Organizes extracted details and drives chatbot interactions.
4. **SQLite Database** - Stores documents, extracted data, and chat history.
5. **Streamlit Frontend** - Provides an intuitive UI for users to upload documents, view extracted details, and chat with the assistant.

### **2️⃣ Architecture Diagram**
```plaintext
                    ┌────────────────────┐
                    │    User (Frontend) │
                    └────────▲──────────┘
                             │
                             ▼
       ┌───────────────────────────────┐
       │      Streamlit Frontend       │
       │  - Uploads insurance docs     │
       │  - Displays extracted details │
       │  - Chat interface             │
       └──────────────▲────────────────┘
                      │ API Requests
                      ▼
       ┌───────────────────────────────┐
       │        FastAPI Backend        │
       │  - Routes for document OCR    │
       │  - Chatbot API (GPT-4o)       │
       │  - Stores extracted data      │
       └───────▲──────────▲────────────┘
               │          │
               ▼          ▼
       ┌────────────┐  ┌────────────────┐
       │  OCR (Tesseract) │  │  GPT-4o Chatbot  │
       └────────────┘  └────────────────┘
               ▲          ▲
               │          │
       ┌───────────────────────────┐
       │     SQLite Database       │
       │ - Stores uploaded docs    │
       │ - Saves chat history      │
       └───────────────────────────┘
```

### **3️⃣ Key Design Choices & Justifications**

### **🔹 Backend: FastAPI**
✅ **FastAPI** was chosen because it provides **asynchronous support** (ideal for AI & OCR processing) and is **lightweight & high-performance**.

### **🔹 OCR: Tesseract**
✅ **Tesseract OCR** is **open-source, widely used, and supports multiple languages** for accurate text extraction from PDFs/images.

### **🔹 AI Model: GPT-4o**
✅ **GPT-4o** provides **natural language understanding** for structuring extracted data and handling conversational interactions.

### **🔹 Database: SQLite**
✅ **SQLite** is used because it's lightweight, requires no setup, and is perfect for storing document metadata and chat history.

### **🔹 Frontend: Streamlit**
✅ **Streamlit** allows for **quick development** of an interactive UI, making it ideal for displaying extracted data and chatbot responses.

### **4️⃣ Data Flow Diagram**
```plaintext
User Uploads Document
     │
     ▼
FastAPI Processes Upload
     │
     ▼
OCR Extracts Text → GPT-4o Organizes Data
     │
     ▼
Structured Data Stored in SQLite
     │
     ▼
Streamlit Fetches & Displays Extracted Data
     │
     ▼
User Interacts with Chatbot (GPT-4o)
     │
     ▼
Chatbot Confirms & Validates Details
     │
     ▼
Finalized Data → Form Generation (PDF)
     │
     ▼
User Downloads Completed Form
```

### **5️⃣ Scalability & Future Enhancements**
- **Enhance AI Processing:** Fine-tune AI responses for better accuracy.
- **Cloud Storage Integration:** Store processed documents on AWS S3 or Google Cloud.
- **Database Optimization:** Switch to **PostgreSQL** for better scalability.
- **User Authentication:** Add user login & document history tracking.
- **Deploy on Kubernetes:** For horizontal scaling in production.

---

## Demo Video  
