"""
Setup verification script for Koicha SEO Engine.
Run this FIRST to confirm all API keys and dependencies are working.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PASS = "[OK]"
FAIL = "[FAILED]"
WARN = "[WARN]"

results = []


def check(label: str, passed: bool, detail: str = ""):
    status = PASS if passed else FAIL
    msg = f"  {status} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    results.append(passed)


print("\nKoicha SEO Engine -- Setup Verification")
print("=" * 50)

# --- 1. Python version ---
print("\n[1] Python Version")
ver = sys.version_info
check("Python 3.11+", ver.major == 3 and ver.minor >= 11,
      f"Found {ver.major}.{ver.minor}.{ver.micro}")

# --- 2. .env file ---
print("\n[2] Environment Variables")
required_vars = [
    "GEMINI_API_KEY",
    "GOOGLE_MAPS_API_KEY",
    "GOOGLE_CLOUD_PROJECT_ID",
    "SITE_BASE_URL",
]
optional_vars = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "KOICHA_SHEET_ID",
    "BLOGGER_BLOG_ID",
]
for var in required_vars:
    val = os.getenv(var)
    check(var, bool(val), "Set" if val else "MISSING — add to .env")

for var in optional_vars:
    val = os.getenv(var)
    if val:
        print(f"  {PASS} {var} — Set")
    else:
        print(f"  {WARN} {var} — Not set yet (needed for later modules)")

# --- 3. Config file ---
print("\n[3] Config File")
config_path = Path("config/koicha_config.json")
check("koicha_config.json exists", config_path.exists())
if config_path.exists():
    with open(config_path) as f:
        cfg = json.load(f)
    check("Brand name", cfg.get("brand", {}).get("name") == "Koicha")
    check("Menu has items", len(cfg.get("menu", {}).get("categories", [])) > 0)

# --- 4. Gemini API ---
print("\n[4] Gemini API")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say 'Koicha verified' in exactly those words.")
    text = response.text.strip()
    check("Gemini API connected", "koicha" in text.lower() or "verified" in text.lower(),
          f"Response: {text[:50]}")
except Exception as e:
    check("Gemini API connected", False, str(e)[:80])

# --- 5. Dependencies ---
print("\n[5] Python Dependencies")
packages = {
    "pdfplumber": "pip install pdfplumber",
    "jinja2": "pip install jinja2",
    "requests": "pip install requests",
    "bs4": "pip install beautifulsoup4",
    "qrcode": "pip install qrcode[pil]",
    "PIL": "pip install Pillow",
    "dotenv": "pip install python-dotenv",
    "google.auth": "pip install google-auth",
    "googleapiclient": "pip install google-api-python-client",
}
for pkg, install_cmd in packages.items():
    try:
        __import__(pkg)
        check(f"{pkg}", True)
    except ImportError:
        check(f"{pkg}", False, f"Run: {install_cmd}")

# --- 6. Directory structure ---
print("\n[6] Directory Structure")
required_dirs = [
    "modules", "templates", "static/schema", "static/css",
    "static/images", "config", "site", "data", "scripts"
]
for d in required_dirs:
    path = Path(d)
    path.mkdir(parents=True, exist_ok=True)
    check(f"/{d}/", True, "Created" if not path.exists() else "OK")

# --- Summary ---
print("\n" + "=" * 50)
passed = sum(results)
total = len(results)
print(f"\n{'All checks passed!' if passed == total else 'Some checks failed'}")
print(f"   {passed}/{total} checks passed\n")

if passed < total:
    print("Fix the FAILED items above, then re-run this script.")
    sys.exit(1)
else:
    print("Ready to run Module 1:")
    print("  python modules/menu_schema_engine.py\n")
