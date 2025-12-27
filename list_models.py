# list_models.py - Check what models are available

import google.generativeai as genai
import os

# Configure with your API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

print("Available Gemini models:\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"  Display name: {model.display_name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()