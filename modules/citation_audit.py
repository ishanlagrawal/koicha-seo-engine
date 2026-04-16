import modules.sheet_utils as sheet_utils
from datetime import datetime

PLATFORMS = {
    "Google Maps": "https://www.google.com/maps/place/KOICHA",
    "Zomato": "https://www.zomato.com/pune/koicha-koregaon-park",
    "Swiggy": "https://www.swiggy.com/restaurants/koicha-pune",
    "Instagram": "https://www.instagram.com/koicha.india/"
}

# The Standard info (The "Truth")
NAP_TRUTH = {
    "name": "KOICHA",
    "address": "Koregaon Park, Pune",
    "phone": "N/A - Direct Online"
}

def run_audit():
    print("\nKoicha Citation Audit -- NAP Consistency Check")
    print("=" * 45)
    
    for platform, url in PLATFORMS.items():
        print(f"Auditing platform: {platform}...")
        
        # In this Zero-Cost version, we flag as "Pending Review" 
        # but link the URL for the user to verify in one click.
        sheet_data = [
            platform,
            "Active",
            "Pending Manual Check",
            url,
            f"Verify if name matches '{NAP_TRUTH['name']}' exactly."
        ]
        sheet_utils.sheet_editor.append_row("Citation_Audit", sheet_data)
        
    print("\n[SUCCESS] Citation Audit log updated in Master Sheet.")

if __name__ == "__main__":
    run_audit()
