import json
import base64

# 1. Leer la base de datos que ya generaste con el builder
try:
    with open("gtfo_db.json", "r") as f:
        db_content = f.read()
except FileNotFoundError:
    print("[-] Error: No encuentro gtfo_db.json. Ejecuta primero el builder.")
    exit()

# 2. El código que vivirá dentro del archivo final
# Nota: Usamos f-strings con precaución o bloques de texto
script_template = r'''import json, sys, os, subprocess, base64

# Base de datos embebida
DB_B64 = "{b64_data}"
db = json.loads(base64.b64decode(DB_B64).decode())

R, G, Y, B, C, W = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[36m", "\033[0m"

def search(binary, method=None, silent=False):
    binary = binary.lower().strip()
    if binary not in db:
        if not silent: print(f"{R}[-] El binario '{binary}' no está en la DB.{W}")
        return
    
    bin_data = db[binary]
    found = False
    for func_name, entries in bin_data.items():
        for entry in entries:
            base_code = entry.get('code')
            contexts = entry.get('contexts', {})
            m_list = [method.lower()] if method else ["sudo", "suid", "shell"]
            for m in m_list:
                if m in contexts:
                    code = contexts[m]['code'] if isinstance(contexts[m], dict) else base_code
                    if code:
                        found = True
                        print(f"\n{Y}[#] MÉTODO: {m.upper()} ({func_name}){W}\n    {C}{code}{W}")
    return found

def auto_scan():
    print(f"{B}[*] Buscando binarios SUID...{W}")
    try:
        bins = subprocess.check_output("find / -perm -u=s -type f 2>/dev/null", shell=True).decode().splitlines()
        for b in [os.path.basename(x) for x in bins]:
            if b in db:
                print(f"{G}[!] VULNERABLE: {b.upper()}{W}")
                search(b, "suid", silent=False)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Y}Uso: python3 {sys.argv[0]} <binario> o --scan{W}")
    elif sys.argv[1] == "--scan":
        auto_scan()
    else:
        search(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
'''

# 3. Insertar la DB en el template y guardar
print("[*] Empaquetando 453 binarios en un solo archivo...")
b64_db = base64.b64encode(db_content.encode()).decode()
final_code = script_template.replace("{b64_data}", b64_db)

with open("gtfo_final.py", "w") as f:
    f.write(final_code)

print("[+] ÉXITO: Se ha creado 'gtfo_final.py'.")
print("[i] Ahora puedes mover 'gtfo_final.py' a cualquier máquina y funcionará solo.")
