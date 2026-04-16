# How-To Guide: Setting Up Automation IDs
=======================================

This guide tracks all specific IDs and configurations needed for the Koicha SEO Engine. 

---

## 🏁 CURRENT ENGINE STATUS
- **Telegram Bot:** ✅ ACTIVE
- **Blogger Automation:** ✅ ACTIVE
- **Google Drive Photos:** ✅ ACTIVE (Syncing from Private)
- **Google Sheets Master:** ✅ ACTIVE (Connected)
- **Google Maps (GBP):** ⚠️ PENDING (Restricted API access)

---

## 1. Telegram Chat ID
**Status:** ✅ COMPLETE
- **Action:** Added `TELEGRAM_CHAT_ID` to `.env`.
- **Bot:** `@KoichaSEO_Bot`.

## 2. Blogger Blog ID
**Status:** ✅ COMPLETE
- **Action:** Added `BLOGGER_BLOG_ID` to `.env`.
- **URL:** [koichapune.blogspot.com](https://koichapune.blogspot.com/)

## 3. Google Sheet Master ID
**Status:** ✅ COMPLETE
- **Action:** Created Sheet "Koicha Digital Master".
- **Security:** Shared the sheet with the Service Account email.
- **Verification:** Engine successfully connected on 2026-04-16.

## 4. Google Drive Assets Folder
**Status:** ✅ COMPLETE
- **Action:** Pointed the engine to the direct "Photos" subfolder.
- **Security:** Engine uses OAuth2 to pull photos from your private folder (No need to make folder public).

- **Constraint:** Currently restricted by Google. Quota is 0 until we apply for full API access.

### 🔄 ZERO-COST WORKAROUND: Metricool
Since the official API is restricted, we use **Metricool** to bridge the gap:
1. **Signup:** Create a free account at [Metricool.com](https://metricool.com/).
2. **Connect:** Use the Official Koicha Email to link your Google Business Profile.
3. **Weekly Sync:**
   - Run the Koicha Engine to generate new articles (`data/articles/`).
   - Copy the text and photo to Metricool's scheduler once a week.

## 6. Google Cloud Setup (GCP)
**Status:** ✅ COMPLETE
- **Project:** `[GCP_PROJECT_ID]`
- **Steps Taken:**
  1. Configured OAuth Consent Screen.
  2. Downloaded and renamed `client_secrets.json`.
  3. Ran `scripts/auth_blogger.py` to generate `token.pickle`.
  4. Added the following Scopes:
     - `blogger`
     - `drive.readonly`
     - `business.manage` (Awaiting Google approval)

---

## 💡 MAINTENANCE: Adding new Photos
Just drop your new artisan food photos into the Drive Folder linked in our Private Assets. The Engine will automatically find them and pick a random one for your next blog post!
