import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Checking models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        try:
            model = genai.GenerativeModel(m.name)
            response = model.generate_content("test")
            print(f"WORKS: {m.name}")
        except Exception as e:
            print(f"FAILS: {m.name} - {str(e)[:50]}")
