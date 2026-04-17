import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini_2_0():
    print("Testing Gemini 2.0 Flash...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[FAIL] GEMINI_API_KEY is missing in .env")
        return False
        
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Confirm you are Gemini 2.0 Flash and say 'Matcha is Ready'."
        )
        print(f"[SUCCESS] Response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_2_0()
