import wikipedia
import json
import sys
import os
import re

def get_dimensions(site_name, wikipedia_url=""):
    print(f"🔍 Suche technische Daten für: {site_name}")
    os.makedirs("Data", exist_ok=True)
    
    dimensions = {"height": None, "diameter": None, "coordinates": None}
    
    try:
        if wikipedia_url:
            title = wikipedia_url.split("/")[-1]
            page = wikipedia.page(title, auto_suggest=False)
        else:
            search = wikipedia.search(site_name, results=3)
            if search:
                page = wikipedia.page(search[0], auto_suggest=False)
            else:
                print("  ⚠ Keine Wikipedia-Seite gefunden")
                return dimensions
        
        print(f"  ✓ Gefunden: {page.title}")
        content = page.content
        
        for pattern in [r'height[:\s]+(\d+(?:\.\d+)?)\s*(m|meter)', r'Höhe[:\s]+(\d+(?:\.\d+)?)\s*m']:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dimensions["height"] = float(match.group(1))
                print(f"  ✓ Höhe: {dimensions['height']}m")
                break
                
        for pattern in [r'diameter[:\s]+(\d+(?:\.\d+)?)\s*(m|meter)', r'Durchmesser[:\s]+(\d+(?:\.\d+)?)\s*m']:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dimensions["diameter"] = float(match.group(1))
                print(f"  ✓ Durchmesser: {dimensions['diameter']}m")
                break
                
        if page.coordinates:
            dimensions["coordinates"] = {"lat": page.coordinates[0], "lon": page.coordinates[1]}
            
        with open("Data/dimensions.json", "w") as f:
            json.dump(dimensions, f, indent=2)
            
    except Exception as e:
        print(f"  ✗ Fehler: {e}")

if __name__ == "__main__":
    site_name = sys.argv[1] if len(sys.argv) > 1 else "Peenemünde"
    wikipedia_url = sys.argv[2] if len(sys.argv) > 2 else ""
    get_dimensions(site_name, wikipedia_url)
