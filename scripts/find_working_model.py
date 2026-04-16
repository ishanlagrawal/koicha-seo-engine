import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Searching for a working model...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Testing model: {m.name}")
        try:
            model = genai.GenerativeModel(m.name)
            response = model.generate_content("Hi")
            print(f"✅ Success with: {m.name}")
            break
        except Exception as e:
            print(f"❌ Failed with {m.name}: {e}")
