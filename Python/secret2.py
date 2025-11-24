# Importo las Librerias
from cryptography.fernet import Fernet

# Carga la clave
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Lee el contenido del JSON
with open("secret.json", "rb") as file:
    original = file.read()

# Encripta y guarda
encrypted = fernet.encrypt(original)

with open("secret.enc", "wb") as enc_file:
    enc_file.write(encrypted)