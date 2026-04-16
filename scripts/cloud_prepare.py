import os
import base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def prepare_secrets():
    print("\n" + "="*50)
    print("      KOICHA CLOUD MIGRATION HELPER")
    print("="*50)
    print("\nCopy these values into your GitHub Repository Secrets:")
    print("(Settings > Secrets and variables > Actions > New repository secret)\n")

    # 1. token.pickle
    token_path = Path("token.pickle")
    if token_path.exists():
        with open(token_path, "rb") as f:
            encoded_token = base64.b64encode(f.read()).decode('utf-8')
            print(f"--- [SECRET NAME: GOOGLE_TOKEN_PICKLE_BASE64] ---")
            print(encoded_token)
            print("-" * 50 + "\n")
    else:
        print("[WARNING] token.pickle not found. Run auth_blogger.py locally first.\n")

    # 2. Re-echo important .env vars for convenience
    env_vars = [
        "GOOGLE_SERVICE_ACCOUNT_JSON",
        "KOICHA_SHEET_ID",
        "GROQ_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "GEMINI_API_KEY",
        "KOICHA_WHATSAPP"
    ]

    for var in env_vars:
        val = os.getenv(var)
        if val:
            print(f"--- [SECRET NAME: {var}] ---")
            print(val)
            print("-" * 50 + "\n")
        else:
            print(f"[MISSING] {var} not found in .env\n")

    print("="*50)
    print("Migration guide: Copy each block above into its respective GitHub Secret.")
    print("Once done, run 'git push' and the Cloud Watchdog will start!")
    print("="*50)

if __name__ == "__main__":
    prepare_secrets()
