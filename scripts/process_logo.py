from PIL import Image, ImageDraw, ImageOps
import os

# Source path (most recent upload)
INPUT_PATH = r"C:\Users\Admin\.gemini\antigravity\brain\428d95be-f572-4594-a770-9d0428a2d2f2\media__1776343634206.png"
OUTPUT_PATH = "static/images/koicha_logo_round.png"

def make_round():
    print(f"Opening logo at {INPUT_PATH}...")
    img = Image.open(INPUT_PATH).convert("RGBA")
    
    # Square off the image (centered crop)
    size = min(img.size)
    img = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    
    # Create circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask and transparency
    round_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    round_img.paste(img, (0, 0), mask=mask)
    
    # Save as PNG
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    round_img.save(OUTPUT_PATH, "PNG")
    print(f"[SUCCESS] Round logo saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    make_round()
