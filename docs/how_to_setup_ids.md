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
**Status:** ✅ FOUND (`5956974216578086430`)

**How it was found:**
1.  Created the blog at `koichapune.blogspot.com`.
2.  Retrieved the ID from the URL and added it to `.env`.

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
**Status:** ✅ VERIFIED (Blogger & GitHub)

**Verification History:**
1.  **Blogger:** Auto-linked as the same account was used.
2.  **GitHub:** Verified via HTML meta tag in `base.html` after correcting a URL mismatch.

---

## 6. Google Cloud Console (OAuth & Automation)
**Status:** ⏳ IN PROGRESS

This is required for the engine to post directly to Blogger/Maps without manual login.

**Steps Completed:**
1.  Enabled **Blogger API v3** in GCP Project `credible-spark-465804-j5`.
2.  Configured **OAuth Consent Screen** (External mode).
3.  Added `koicha.india.digital@gmail.com` and personal email as **Test Users**.
4.  Added personal email as an **Admin/Author** on Blogger Settings.

**Next Step:**
1.  Go to **Credentials > + Create Credentials > OAuth client ID**.
2.  Choose **Desktop App**.
3.  Download the JSON, rename it to `client_secrets.json`, and place it in the project root.
