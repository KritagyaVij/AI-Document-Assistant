# gemini_service.py

import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure API key
genai.configure(api_key=GEMINI_API_KEY)

# Use the correct working model
model = genai.GenerativeModel("gemini-2.5-flash")


def get_gemini_response(user_message: str) -> str:
    try:
        response = model.generate_content(user_message)

        # Return clean text
        if response.text:
            return response.text
        else:
            return "No response generated."

    except Exception as e:
        return f"Gemini API Error: {str(e)}"
