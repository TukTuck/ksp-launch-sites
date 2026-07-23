import requests
import json
import sys
import os

def generate_blender_script(site_name, hf_token):
    print(f"🤖 Generiere Blender-Skript für: {site_name}")
    
    dimensions = {}
    if os.path.exists("Data/dimensions.json"):
        with open("Data/dimensions.json", "r") as f:
            dimensions = json.load(f)
            
    API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
    
    prompt = f"""
Erstelle ein vollständiges Blender Python-Skript für die Launch Site: {site_name}
Technische Daten: Höhe: {dimensions.get('height', 'unbekannt')}m, Durchmesser: {dimensions.get('diameter', 'unbekannt')}m.
Das Skript soll Hauptstrukturen als Zylinder/Boxen modellieren, Materialien erstellen und Kommentare auf Deutsch haben.
Gib NUR den Python-Code zurück.
"""
    
    headers = {"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 2048, "return_full_text": False}}
    
    print("  📡 Sende Anfrage an Hugging Face...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        script = result[0].get('generated_text', '') if isinstance(result, list) else result.get('generated_text', '')
        script = script.replace("```python", "").replace("```", "").strip()
        
        os.makedirs("Scripts", exist_ok=True)
        safe_name = site_name.replace(" ", "_").replace("/", "_")
        filename = f"Scripts/blender_{safe_name}.py"
        
        with open(filename, "w") as f:
            f.write(script)
        print(f"  ✓ Blender-Skript gespeichert: {filename}")
    else:
        print(f"  ✗ API Fehler: {response.status_code} - {response.text}")

if __name__ == "__main__":
    site_name = sys.argv[1]
    token = sys.argv[2]
    generate_blender_script(site_name, token)
