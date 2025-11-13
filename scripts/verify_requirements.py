# scripts/verify_requirements.py

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = BASE_DIR.parent / "requirements.txt"
LOG_FILE = BASE_DIR.parent / "data" / "outputs" / "logs" / "verify_requirements.log"

# --- Funciones ---
def read_requirements(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo requirements.txt no encontrado en {file_path}")
    with open(file_path, "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return packages

def check_package(pkg: str):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False

def install_package(pkg: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def log(message: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def verify_requirements(auto_install=False):
    packages = read_requirements(REQUIREMENTS_FILE)
    missing = []

    for pkg in packages:
        pkg_name = pkg.split("==")[0]  # Para paquetes con versión
        if not check_package(pkg_name):
            missing.append(pkg)
            log(f"[WARNING] Paquete faltante: {pkg}")
            if auto_install:
                try:
                    log(f"[INFO] Instalando {pkg}...")
                    install_package(pkg)
                    log(f"[INFO] Paquete instalado: {pkg}")
                except Exception as e:
                    log(f"[ERROR] Error instalando {pkg}: {e}")

    if not missing:
        log("[INFO] Todas las librerías están instaladas correctamente.")
    else:
        log(f"[INFO] Paquetes faltantes: {missing}")

# --- Ejecución ---
if __name__ == "__main__":
    verify_requirements(auto_install=True)
