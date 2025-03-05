from utils.openai_client import generate_response
from models.conversation import Conversation, SessionLocal
from sqlalchemy import text

def validate_data(field: str, value: str) -> bool:
    if field == "name":
        return value.isalpha()
    if field == "status":
        return value.lower() in ["active", "inactive"]
    if field == "policy_end":
        from datetime import datetime
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return True

async def get_conversation_state(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            text("SELECT state FROM conversations WHERE user_id = :user_id ORDER BY id DESC LIMIT 1"),
            {"user_id": user_id}
        )
        state = result.scalar()
        return state or "start"


async def update_conversation_state(user_id: int, state: str, question: str = "N/A"):
    async with SessionLocal() as session:
        new_conversation = Conversation(user_id=user_id, question=question, state=state)
        session.add(new_conversation)
        await session.commit()

async def handle_user_message(user_id: int, message: str):
    state = await get_conversation_state(user_id)
    if state == "start":
        prompt = f"User wants to fill out an insurance form. Start by asking for their name. User said: {message}"
        next_state = "ask_name"
    elif state == "ask_name":
        prompt = f"User provided their name: {message}. Ask for insurance status (Active/Inactive)."
        next_state = "ask_status"
    elif state == "ask_status":
        prompt = f"User provided insurance status: {message}. Ask for policy end date."
        next_state = "ask_policy_end"
    elif state == "ask_policy_end":
        prompt = f"User provided policy end date: {message}. Ask for copay details (Consultation, Pharma, Physio, etc.)."
        next_state = "ask_copay"
    else:
        prompt = f"User provided: {message}. Confirm all details and proceed to form generation."
        next_state = "confirm"

    response = await generate_response(prompt)
    await update_conversation_state(user_id, next_state)

    return response

