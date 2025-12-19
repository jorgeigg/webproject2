import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # carpeta temporal de PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ejemplo de uso
secret_file = resource_path("secret.key")
with open(secret_file, "rb") as f:
    clave = f.read()
# ***********************
import sys
import os

def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta al recurso.
    Compatible con ejecución normal y con PyInstaller (--onefile).
    """
    try:
        # Cuando se ejecuta empaquetado con PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Cuando se ejecuta en modo normal (fuentes)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- Uso para tu archivo secret.key ---
secret_file = resource_path("secret.key")

with open(secret_file, "rb") as key_file:
    key = key_file.read()

#print("Clave cargada correctamente:", key[:10], "...")  # muestra solo los primeros bytes
