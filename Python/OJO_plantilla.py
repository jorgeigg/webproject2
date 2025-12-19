import sys
import os
import logging

# --- Configuración de logging ---
logging.basicConfig(
    filename="app.log",        # archivo donde se guardan los logs
    level=logging.DEBUG,       # nivel de detalle
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Aplicación iniciada")

# --- Manejo de recursos en --onefile ---
def resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller --onefile.
    """
    try:
        # Cuando se ejecuta empaquetado con PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Cuando se ejecuta en modo normal (fuentes)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ejemplo: cargar un archivo de configuración
config_file = resource_path("config.json")
logging.info(f"Usando archivo de configuración: {config_file}")
# Supongamos que tienes varios archivos de configuración
config_json = resource_path("config.json")
db_config = resource_path("db_config.json")
ui_config = resource_path("ui_config.yaml")

print("Config principal:", config_json)
print("Config base de datos:", db_config)
print("Config interfaz:", ui_config)
# --- Lógica principal ---
def main():
    logging.info("Entrando en main()")
    print("Hola Jorge, tu ejecutable funciona correctamente 🚀")

if __name__ == "__main__":
    main()