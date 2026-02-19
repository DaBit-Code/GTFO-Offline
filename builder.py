import os
import yaml
import json
import subprocess
import shutil

REPO_URL = "https://github.com/GTFOBins/GTFOBins.github.io.git"
TEMP_DIR = "gtfo_repo"
DB_FILE = "gtfo_db.json"

def build_db():
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        
        print(f"[*] Clonando GTFOBins (Full Clone)...")
        # Clonamos completo sin --depth 1 para evitar archivos faltantes
        subprocess.run(["git", "clone", REPO_URL, TEMP_DIR], check=True, capture_output=True)

        database = {}
        
        print("[*] Rastreando archivos de binarios en todo el repositorio...")
        
        for root, dirs, files in os.walk(TEMP_DIR):
            if '.git' in root: continue
            
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Intentamos leer archivos que no sean imágenes/binarios
                if filename.endswith(('.md', '.yml', '')): 
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # La marca de identidad de un archivo de GTFOBins es el YAML con 'functions:'
                            if 'functions:' in content and '---' in content:
                                parts = content.split('---')
                                yaml_part = parts[1] if len(parts) > 1 else parts[0]
                                
                                data = yaml.safe_load(yaml_part)
                                if data and 'functions' in data:
                                    # El nombre suele estar en el filename o en una clave 'bin'
                                    bin_name = data.get('bin', filename.split('.')[0])
                                    database[bin_name] = data['functions']
                                    print(f"[+] Detectado: {bin_name}")
                    except:
                        continue

        if not database:
            print("[-] No se detectó ningún binario válido. Algo va muy mal con el clon.")
            return

        with open(DB_FILE, 'w') as f:
            json.dump(database, f, indent=4)
        
        print(f"\n[!] VICTORIA. Base de datos: {DB_FILE} ({len(database)} binarios)")

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    build_db()
