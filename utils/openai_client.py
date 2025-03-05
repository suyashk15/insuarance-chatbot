import openai
from config import OPENAI_API_KEY
import json, re

openai.api_key = OPENAI_API_KEY

async def generate_response(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an insurance document assistant. Extract details and return ONLY valid JSON. Do NOT include markdown code blocks or extra text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        temperature=0
    )

    try:
        content = response["choices"][0]["message"]["content"].strip()

        print("GPT-4o Response:", repr(content))

        content = re.sub(r"^```json\n|\n```$", "", content.strip(), flags=re.MULTILINE)

        return json.loads(content)

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse GPT-4o response: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
