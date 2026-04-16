import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    print("\n--- Testing Gemini API ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[FAILED] No GEMINI_API_KEY found in .env")
        return
    
    try:
        genai.configure(api_key=api_key)
        print("Listing available Gemini Models...")
        models = genai.list_models()
        count = 0
        for m in models:
            print(f"  - {m.name} (supports: {m.supported_generation_methods})")
            count += 1
        
        if count == 0:
            print("[WARN] Connected, but 0 models returned. This might be a restriction on your API key.")
        else:
            print(f"[OK] Success! Found {count} models.")
            
    except Exception as e:
        print(f"[FAILED] Gemini API Error: {e}")

def test_groq():
    print("\n--- Testing Groq API ---")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[FAILED] No GROQ_API_KEY found in .env")
        return
    
    try:
        import requests
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
        if response.status_code == 200:
            models = response.json().get("data", [])
            print(f"[OK] Success! Found {len(models)} Groq models:")
            for m in models:
                print(f"  - {m['id']}")
        else:
            print(f"[FAILED] Groq API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[FAILED] Groq Error: {e}")

if __name__ == "__main__":
    test_gemini()
    test_groq()
