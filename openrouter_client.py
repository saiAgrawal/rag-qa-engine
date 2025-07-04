from dotenv import load_dotenv
import requests
import os

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = "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"

        print("🔑 API Key Loaded:", self.api_key)  # Debug
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-7b-instruct"


    def generate_response(self, prompt, context=""):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer based only on the context."}
        ]

        payload = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            return f"❌ OpenRouter Error: {response.text}"
        except Exception as e:
            return f"❌ Request Failed: {e}"
