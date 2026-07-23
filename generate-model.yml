from duckduckgo_search import DDGS
import requests
import os
import sys
from PIL import Image
from io import BytesIO

def search_and_download(site_name, max_images=50):
    print(f"🔍 Suche nach: {site_name}")
    safe_name = site_name.replace(" ", "_").replace("/", "_")
    os.makedirs(f"References/{safe_name}", exist_ok=True)
    
    results = DDGS().images(site_name, max_results=int(max_images))
    downloaded = 0
    
    for i, result in enumerate(results):
        try:
            print(f"  Lade Bild {i+1}...")
            response = requests.get(result['image'], timeout=10)
            img = Image.open(BytesIO(response.content))
            
            if img.width < 512 or img.height < 512:
                print(f"    ⊘ Zu klein ({img.width}x{img.height})")
                continue
            
            filename = f"References/{safe_name}/{i:03d}_{img.width}x{img.height}.jpg"
            img.save(filename, "JPEG", quality=95)
            downloaded += 1
            print(f"    ✓ Gespeichert ({img.width}x{img.height})")
        except Exception as e:
            print(f"    ✗ Fehler: {e}")
    
    print(f"\n✅ Fertig! {downloaded} Bilder gespeichert in References/{safe_name}/")

if __name__ == "__main__":
    site_name = sys.argv[1] if len(sys.argv) > 1 else "Peenemünde"
    max_images = sys.argv[2] if len(sys.argv) > 2 else "50"
    search_and_download(site_name, max_images)
