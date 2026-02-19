import json
import sys
import os
import subprocess

DB_FILE = "gtfo_db.json"
R, G, Y, B, C, W = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[36m", "\033[0m"

def get_suid_bins():
    """Busca binarios SUID en el sistema"""
    print(f"{B}[*] Buscando binarios SUID en el sistema...{W}")
    try:
        # Ejecutamos find para buscar SUIDs, silenciando errores de permiso
        cmd = "find / -perm -u=s -type f 2>/dev/null"
        output = subprocess.check_output(cmd, shell=True).decode().splitlines()
        return [os.path.basename(b) for b in output]
    except:
        return []

def auto_scan(db):
    """Cruza los binarios del sistema con la base de datos"""
    suid_bins = get_suid_bins()
    found_any = False

    print(f"{B}[*] Comparando con la base de datos de GTFOBins...{W}\n")
    
    for bin_name in suid_bins:
        if bin_name in db:
            found_any = True
            print(f"{G}[!] VULNERABLE: {W}{C}{bin_name.upper()}{W} (SUID detectado)")
            # Mostramos el comando de explotación para SUID directamente
            search(bin_name, "suid", silent=True)
            print("-" * 40)
            
    if not found_any:
        print(f"{Y}[-] No se encontraron binarios SUID conocidos en la DB.{W}")

def search(binary, method=None, silent=False):
    try:
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        if not silent: print(f"{R}[-] Error: No se encuentra {DB_FILE}{W}")
        return None

    if not silent and method == "--scan":
        auto_scan(db)
        return

    binary = binary.lower().strip()
    if binary not in db:
        if not silent: print(f"{R}[-] El binario '{binary}' no está en la DB.{W}")
        return

    if not silent: print(f"\n{B}=== GTFOBins Local: {C}{binary.upper()} {B}==={W}")
    
    bin_data = db[binary]
    found = False

    for func_name, entries in bin_data.items():
        for entry in entries:
            base_code = entry.get('code')
            contexts = entry.get('contexts', {})
            
            methods_to_check = [method.lower()] if method else ["sudo", "suid", "shell", "capabilities"]
            
            for m in methods_to_check:
                if m in contexts:
                    if isinstance(contexts[m], dict) and 'code' in contexts[m]:
                        found = True
                        print(f"{Y}[#] MÉTODO: {m.upper()} ({func_name}){W}")
                        print(f"    {C}{contexts[m]['code']}{W}")
                    elif m in contexts and base_code:
                        found = True
                        print(f"{Y}[#] MÉTODO: {m.upper()} ({func_name}){W}")
                        print(f"    {C}{base_code}{W}")

    if not found and not silent:
        print(f"{R}[-] No se encontró el método '{method}' para este binario.{W}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Y}Uso: python3 gtfo.py <binario> [metodo]{W}")
        print(f"Opcional: python3 gtfo.py --scan{W}")
    elif sys.argv[1] == "--scan":
        search("", "--scan")
    else:
        met = sys.argv[2] if len(sys.argv) > 2 else None
        search(sys.argv[1], met)
