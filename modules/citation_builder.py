"""
Module 6: Citation Builder (Blogger)
====================================
Automates posting SEO articles to Blogger.com.
Creates a local citation footprint (Backlinks + Keywords).
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

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
    except Exception as e:
        print(f"[ERROR] Error posting to Blogger: {str(e)}")

def generate_article(topic_key: str, config: dict) -> dict:
    """Uses Groq to write a high-SEO article about Koicha."""
    print(f"Generating article for topic: {topic_key}...")
    
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
    
    ARTICLE_DIR = Path("data/articles")
    ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
    
    for topic in ["matcha", "food"]:
        article = generate_article(topic, config)
        filename = f"{topic}.md"
        with open(ARTICLE_DIR / filename, "w", encoding="utf-8") as f:
            f.write(f"# {article['title']}\n\n{article['content']}")
        print(f"Draft Saved: {ARTICLE_DIR}/{filename}")
        
        if BLOG_ID:
            print(f"Posting '{topic}' to Blogger...")
            post_to_blogger(article['title'], article['content'], BLOG_ID)
    
    print("\nModule 6: Initial Citation Blast Complete!")

if __name__ == "__main__":
    run()
