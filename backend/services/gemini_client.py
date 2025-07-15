# gemini_client.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, prompt, context=""):
        full_prompt = f"""
You are a helpful assistant. Use the context below to answer the user's question.

Context:
{context}

Question:
{prompt}

Answer in 2-3 clear sentences.
"""

        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"❌ Gemini Error: {e}"