from duckduckgo_search import DDGS
import requests
import os
import sys
from PIL import Image
from io import BytesIO

def search_and_download(site_name, max_images):
    print("Suche nach:", site_name)
    safe_name = site_name.replace(" ", "_").replace("/", "_")
    folder = "References/" + safe_name
    os.makedirs(folder, exist_ok=True)

    results = DDGS().images(site_name, max_results=int(max_images))
    downloaded = 0

    for i, result in enumerate(results):
        try:
            response = requests.get(result['image'], timeout=10)
            img = Image.open(BytesIO(response.content))
            if img.width < 512 or img.height < 512:
                continue
            filename = folder + "/" + str(i).zfill(3) + "_" + str(img.width) + "x" + str(img.height) + ".jpg"
            img.save(filename, "JPEG", quality=95)
            downloaded += 1
            print("OK:", filename)
        except Exception as e:
            print("Fehler bei Bild", i, ":", e)

    print("Fertig!", downloaded, "Bilder gespeichert.")

if __name__ == "__main__":
    site_name = sys.argv[1]
    max_images = sys.argv[2]
    search_and_download(site_name, max_images)
