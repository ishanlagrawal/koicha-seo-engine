# How-To Guide: Setting Up Automation IDs

This guide explains how to get the specific IDs needed for the Koicha SEO Engine to automate Google and Telegram interactions.

---

## 1. Telegram Chat ID
**Current Status:** ✅ FOUND (`1477581734`)

**How it was found:**
1.  Shared a message with the bot `KoichaSEO_Bot`.
2.  Ran `scripts/get_chat_id.py` to pull the latest interaction ID.
3.  Updated `.env` with `TELEGRAM_CHAT_ID=1477581734`.

---

## 2. Blogger Blog ID
**Status:** ⏳ PENDING

**Steps to get it:**
1.  Visit [Blogger.com](https://www.blogger.com/).
2.  Create a blog titled `Koicha — Korean Food & Matcha Pune`.
3.  Choose a URL like `koichapune.blogspot.com`.
4.  Copy the long string of numbers at the very end of your browser's URL while on the Blogger dashboard.
5.  Add to `.env` as `BLOGGER_BLOG_ID`.

---

## 3. Google Sheet Master ID
**Status:** ⏳ PENDING

**Steps to get it:**
1.  Create a new Google Sheet.
2.  Name it `Koicha SEO Content Master`.
3.  Look at the browser URL: `https://docs.google.com/spreadsheets/d/1abc123.../edit`
4.  The string between `/d/` and `/edit` is your ID.
5.  Share the sheet with the Service Account email found in your `.secret` or GCP console.
6.  Add to `.env` as `KOICHA_SHEET_ID`.

---

## 4. Google Business Profile (GBP) Access
**Status:** ⏳ PENDING

**Steps to get it:**
1.  Ask the owner to go to [Business Profile Manager](https://business.google.com/).
2.  Settings -> Users -> Add User.
3.  Invite your dedicated "Engine" email as **Manager**.

---

## 5. Google Search Console
**Status:** ⏳ PENDING (Blogger: DONE)

**Steps for Blogger:**
1.  Blogger Auto-Links: If logged into the same Google account, Blogger automatically adds your site to GSC.
2.  Go to [Google Search Console](https://search.google.com/search-console).
3.  Click "Add Property" > "URL Prefix".
4.  Enter `https://koichapune.blogspot.com` (your URL).
5.  Click "Continue" (Auto-verified).

**Steps for GitHub Pages:**
1.  In GSC, click "Add Property" > "URL Prefix".
2.  Enter `https://ishanlagrawal.github.io/koicha-seo-engine/`.
3.  Click "Continue".
4.  Choose "HTML tag" verification method.
5.  Copy the `<meta>` tag provided.
6.  Paste it into `templates/base.html` inside the `<head>` section.
7.  Run `python modules/site_builder.py` to rebuild.
8.  Push code to GitHub.
9.  Click "Verify" in GSC.
