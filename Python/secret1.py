# Importo las Librerias
from cryptography.fernet import Fernet

# Genera una clave secreta
key = Fernet.generate_key()

# Guarda la clave en un archivo (solo una vez)
with open("secret.key", "wb") as key_file:
    key_file.write(key)