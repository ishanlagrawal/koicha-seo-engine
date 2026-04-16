import fitz
import os
from pathlib import Path

# Path configuration
PDF_PATH = Path("data/koicha-menu.pdf.pdf")
OUTPUT_DIR = Path("static/images/extracted_logo")

def extract_logo():
    print(f"Opening {PDF_PATH}...")
    if not PDF_PATH.exists():
        print(f"[ERROR] PDF not found at {PDF_PATH}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(str(PDF_PATH))
    print(f"Total Pages: {len(doc)}")
    
    # We focus on the first 2 pages for the logo
    for i in range(min(2, len(doc))):
        page = doc.load_page(i)
        image_list = page.get_images(full=True)
        
        print(f"Page {i+1}: Found {len(image_list)} images.")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"image_p{i+1}_{img_index}.{image_ext}"
            image_path = OUTPUT_DIR / image_filename
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            print(f"  [SAVED] {image_filename} ({len(image_bytes) / 1024:.1f} KB)")

    doc.close()
    print(f"\nExtraction complete. Images are in {OUTPUT_DIR}/")

if __name__ == "__main__":
    extract_logo()
