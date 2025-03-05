import streamlit as st
import requests
import pandas as pd

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Insurance Chatbot", layout="wide")

st.markdown("<h1 style='text-align: center;'>📄 AI-Powered Insurance Chatbot</h1>", unsafe_allow_html=True)
st.divider()

# --- SECTION 1: Upload Insurance Document ---
st.markdown("### 📂 Upload Insurance Document")

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

col1, col2 = st.columns([3, 2])
with col1:
    if uploaded_file is not None:
        with st.spinner("Processing document... ⏳"):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{FASTAPI_URL}/documents/upload/", files=files)

        if response.status_code == 200:
            extracted_data = response.json()["data"]
            st.success("✅ Document processed successfully!")
        else:
            st.error("❌ Failed to process document.")
            extracted_data = None
    else:
        extracted_data = None

# --- SECTION 2: Show Extracted Details in Table ---
st.markdown("### 📑 Extracted Insurance Details")

def display_extracted_data(data):
    """Convert JSON into a table format."""
    for key, value in data.items():
        if isinstance(value, dict):
            st.markdown(f"#### {key.replace('_', ' ').title()}")
            df = pd.DataFrame(value.items(), columns=["Field", "Value"])
            st.table(df)
        elif isinstance(value, list):
            st.markdown(f"#### {key.replace('_', ' ').title()}")
            for item in value:
                st.write(f"- {item}")
        else:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")

if extracted_data:
    display_extracted_data(extracted_data)
else:
    st.info("Upload a document to see extracted details.")

st.divider()

# --- SECTION 3: Chatbot for Data Validation ---
st.markdown("### 🤖 Chat with the Insurance Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()
with chat_container:
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.write(message)

user_input = st.text_input("Enter a message to chat with the assistant:")

if st.button("Send"):
    if user_input:
        with st.spinner("Chatbot is thinking... 💬"):
            chat_response = requests.post(
                f"{FASTAPI_URL}/chatbot/chat/",
                json={"user_id": 1, "message": user_input},
            )

        if chat_response.status_code == 200:
            bot_reply = chat_response.json()["response"]
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", bot_reply))
            st.experimental_rerun()
        else:
            st.error("⚠️ Error communicating with chatbot.")

st.divider()

# --- SECTION 4: Insurance Query ---
st.markdown("### 📢 Ask General Insurance Questions")

query_input = st.text_input("Enter your insurance-related question:")
if st.button("Ask"):
    if query_input:
        with st.spinner("Fetching answer... 🤖"):
            query_response = requests.post(
                f"{FASTAPI_URL}/chatbot/chat/",
                json={"user_id": 1, "message": query_input},
            )

        if query_response.status_code == 200:
            st.success("**Chatbot:** " + query_response.json()["response"])
        else:
            st.error("❌ Error retrieving response.")
