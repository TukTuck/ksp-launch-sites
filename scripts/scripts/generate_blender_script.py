import requests
import json
import sys
import os

def generate(site_name, hf_token):
    print("Generiere Blender-Skript fuer:", site_name)

    dimensions = {}
    if os.path.exists("Data/dimensions.json"):
        with open("Data/dimensions.json", "r") as f:
            dimensions = json.load(f)

    height = dimensions.get("height", "unbekannt")
    diameter = dimensions.get("diameter", "unbekannt")

    prompt = (
        "Erstelle ein Blender-Python-Skript fuer die Launch Site " + site_name + ". "
        "Hoehe: " + str(height) + " Meter. Durchmesser: " + str(diameter) + " Meter. "
        "Modelliere Hauptstrukturen als Zylinder und Boxen. "
        "Erstelle Materialien fuer Beton und Metall. "
        "Gib NUR den Python-Code zurueck, keine Erklaerungen."
    )

    api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
    headers = {
        "Authorization": "Bearer " + hf_token,
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 2048, "return_full_text": False}
    }

    print("Sende Anfrage an Hugging Face...")
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code != 200:
        print("API Fehler:", response.status_code)
        print(response.text)
        return

    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        script = result[0].get("generated_text", "")
    elif isinstance(result, dict):
        script = result.get("generated_text", "")
    else:
        script = str(result)

    script = script.replace("```python", "").replace("```", "").strip()

    os.makedirs("Scripts", exist_ok=True)
    safe_name = site_name.replace(" ", "_").replace("/", "_")
    filename = "Scripts/blender_" + safe_name + ".py"

    with open(filename, "w") as f:
        f.write(script)

    print("Skript gespeichert:", filename)

if __name__ == "__main__":
    site_name = sys.argv[1]
    hf_token = sys.argv[2]
    generate(site_name, hf_token)
