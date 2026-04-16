import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_chat_id():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env")
        return

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    print("Checking for recent messages to your bot...")
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data.get("ok"):
            print(f"Telegram API Error: {data}")
            return

        results = data.get("result", [])
        if not results:
            print("\nNo messages found! Please go to Telegram and send a message to your bot first.")
            print("Then run this script again.")
            return

        # Get the latest chat ID
        last_update = results[-1]
        chat_id = last_update["message"]["chat"]["id"]
        username = last_update["message"]["chat"].get("first_name", "User")
        
        print("\n" + "="*30)
        print(f"SUCCESS! Found your Chat ID.")
        print(f"User: {username}")
        print(f"Chat ID: {chat_id}")
        print("="*30)
        print("\nACTION: Copy this number into your .env file as TELEGRAM_CHAT_ID")
        
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")

if __name__ == "__main__":
    get_chat_id()
