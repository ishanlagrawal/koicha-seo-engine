"""
Module 6: Citation Builder (Blogger)
====================================
Automates posting SEO articles to Blogger.com.
Creates a local citation footprint (Backlinks + Keywords).
"""

import os
import json
import requests
import random
import io
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
API_KEY = os.getenv("GEMINI_API_KEY") # We use API Key for Blogger if public, or OAuth

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def post_to_blogger(title: str, content: str, blog_id: str, image_url: str = None):
    """Posts an article with an optional header image."""
    import pickle
    import os
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Error: Auth required. Run scripts/auth_blogger.py first.")
            return

    import modules.sheet_utils as sheet_utils
    from datetime import datetime

    service = build('blogger', 'v3', credentials=creds)
    
    html_content = content.replace('\n', '<br>')
    if image_url:
        html_content = f'<div style="text-align: center; margin-bottom: 20px;"><img src="{image_url}" style="max-width: 100%; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"></div>' + html_content

    body = {
        'kind': 'blogger#post',
        'title': title,
        'content': html_content
    }
    
    try:
        posts = service.posts()
        request = posts.insert(blogId=blog_id, body=body)
        result = request.execute()
        print(f"[SUCCESS] Successfully posted: {result['url']}")
        
        # Log to Master Sheet [NEW]
        sheet_data = [
            datetime.now().strftime("%Y-%m-%d"),
            "Blogger",
            title,
            result['url'],
            "Live",
            "Korean food, Pune, Matcha"
        ]
        sheet_editor = sheet_utils.KoichaSheetEditor()
        sheet_editor.append_row("Article_Log", sheet_data)
        
    except Exception as e:
        print(f"[ERROR] Error posting to Blogger: {str(e)}")

def delete_redundant_posts(blog_id: str):
    """Deletes old placeholder posts to keep the blog clean."""
    import pickle
    from googleapiclient.discovery import build
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds: return
    service = build('blogger', 'v3', credentials=creds)
    
    try:
        # List all posts
        posts_resp = service.posts().list(blogId=blog_id).execute()
        posts = posts_resp.get('items', [])
        
        # We want to keep ONLY the 2 most recent "Humanized" ones (the ones with images or recent timestamps)
        # For simplicity, we'll keep the top 2 and delete the rest
        if len(posts) > 2:
            to_delete = posts[2:]
            for p in to_delete:
                print(f"Deleting redundant post: {p['title']}...")
                service.posts().delete(blogId=blog_id, postId=p['id']).execute()
            print(f"Cleanup complete. Deleted {len(to_delete)} posts.")
    except Exception as e:
        print(f"Cleanup error: {e}")

def sync_photos_from_drive(creds, folder_id: str):
    """Downloads photos from Google Drive folder to local assets."""
    from googleapiclient.discovery import build
    service = build('drive', 'v3', credentials=creds)
    
    # Create local folder
    out_dir = Path("docs/assets/blog")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Syncing photos from Drive folder: {folder_id}...")
    
    # We use 'shortcutDetails' and better queries to find images anywhere in the hierarchy
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()
    
    items = results.get('files', [])
    downloaded_paths = []
    
    for item in items:
        # If it's a folder, look inside it too
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"Opening subfolder: {item['name']}...")
            sub_results = service.files().list(
                q=f"'{item['id']}' in parents and (mimeType = 'image/jpeg' or mimeType = 'image/png')",
                fields="files(id, name)"
            ).execute()
            items.extend(sub_results.get('files', []))
            continue

        file_path = out_dir / item['name']
        if not file_path.exists():
            print(f"Downloading {item['name']}...")
            request = service.files().get_media(fileId=item['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            with open(file_path, "wb") as f:
                f.write(fh.getvalue())
        
        downloaded_paths.append(f"assets/blog/{item['name']}")
    
    return downloaded_paths

def generate_article(topic_key: str, config: dict) -> dict:
    """Uses Groq to write a high-SEO article about Koicha."""
    print(f"Generating article for topic: {topic_key}...")
    
    brand = config["brand"]
    location = config["location"]
    
    prompts = {
        "matcha": f"Write a personal, soul-stirring story about a rainy morning in {location['neighborhood']}, Pune. The narrator discovers {brand['name']} and watches a bamboo whisk (Chasen) transform green powder from Shizuoka into silk. Speak about the 'Zen' of the process. Avoid corporate jargon. Use terms like 'Matcha Soul' and 'Mindful Sips'. End with a casual 'Drop by when you need to breathe.' and link to {os.getenv('SITE_BASE_URL')}.",
        "food": f"Write a vibrant, first-person foodie adventure through Koregaon Park. Describe the search for 'Real Gimbap'—not the supermarket stuff. Then, the discovery of {brand['name']}'s limited-batch kitchen. Describe the steam, the smell of sesame oil, and the 'life-changing' spice of the Tteokbokki. Use a tone that sounds like a handwritten note. End with 'Find us here: {brand['swiggy_url']}'"
    }
    
    prompt = prompts.get(topic_key, prompts["food"])
    content = groq_generate(prompt)
    
    # Simple title extraction (assuming first line is title or similar)
    title = f"Koicha: {topic_key.capitalize()} Experience in Pune"
    if topic_key == "matcha":
        title = "The Gold Standard of Matcha: Why Koicha Sourcing Matters"
    elif topic_key == "food":
        title = "Artisan Korean Street Food: Why Gimbap is Taking Over Koregaon Park"
        
    return {"title": title, "content": content}

def groq_generate(prompt: str) -> str:
    # Reusing the same logic from site_builder for consistency
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '').strip()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile", # Higher quality for articles
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "Error generating content."

def run():
    print("\nKoicha Citation Builder -- Module 6")
    print("=" * 45)
    config = load_config()
    # 1. Auth and Drive Sync
    import pickle
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    drive_photos = []
    if os.getenv("DRIVE_FOLDER_ID") and creds:
        drive_photos = sync_photos_from_drive(creds, os.getenv("DRIVE_FOLDER_ID"))
    
    # 2. Cleanup
    if BLOG_ID:
        delete_redundant_posts(BLOG_ID)
    
    # 3. Generate and Post
    ARTICLE_DIR = Path("data/articles")
    ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get base URL for images
    base_url = os.getenv("SITE_BASE_URL", "").rstrip("/")
    
    topics = ["matcha", "food"]
    for topic in topics:
        article = generate_article(topic, config)
        
        # Pick a random photo if available
        image_url = None
        if drive_photos:
            photo_path = random.choice(drive_photos)
            import time
            # Adding ?t=... forces the browser to fetch the NEW image immediately
            image_url = f"{base_url}/{photo_path}?t={int(time.time())}"
        
        print(f"Posting '{topic}' to Blogger (Humanized + Hosted Photo)...")
        post_to_blogger(article['title'], article['content'], BLOG_ID, image_url)
    
    print("\nModule 6: Initial Citation Blast Complete!")

if __name__ == "__main__":
    run()
