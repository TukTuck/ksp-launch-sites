import wikipedia
import re
import json
import sys
import os

def get_dimensions(site_name, wikipedia_url):
    print("Suche Daten fuer:", site_name)
    os.makedirs("Data", exist_ok=True)

    dimensions = {"height": None, "diameter": None}

    try:
        if wikipedia_url:
            title = wikipedia_url.split("/")[-1]
            page = wikipedia.page(title, auto_suggest=False)
        else:
            results = wikipedia.search(site_name, results=3)
            if not results:
                print("Keine Wikipedia-Seite gefunden.")
                return
            page = wikipedia.page(results[0], auto_suggest=False)

        print("Gefunden:", page.title)
        content = page.content

        height_patterns = [
            r'height[:\s]+(\d+(?:\.\d+)?)\s*(m|meter|meters)',
            r'Hoehe[:\s]+(\d+(?:\.\d+)?)\s*m',
            r'Höhe[:\s]+(\d+(?:\.\d+)?)\s*m'
        ]
        for pattern in height_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dimensions["height"] = float(match.group(1))
                print("Hoehe:", dimensions["height"])
                break

        diameter_patterns = [
            r'diameter[:\s]+(\d+(?:\.\d+)?)\s*(m|meter)',
            r'Durchmesser[:\s]+(\d+(?:\.\d+)?)\s*m'
        ]
        for pattern in diameter_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                dimensions["diameter"] = float(match.group(1))
                print("Durchmesser:", dimensions["diameter"])
                break

        with open("Data/dimensions.json", "w") as f:
            json.dump(dimensions, f, indent=2)

        print("Daten gespeichert in Data/dimensions.json")

    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    site_name = sys.argv[1]
    wikipedia_url = sys.argv[2] if len(sys.argv) > 2 else ""
    get_dimensions(site_name, wikipedia_url)
