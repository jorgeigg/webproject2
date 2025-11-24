'''
@autor: Jorge Garcia
Created on 11/14/2025
'''
# Programa que crea un archivo Excel con los datos leidos de un PLC S7-1500
# Los datos estan almacenados en una base de datos PostgreSQL
import os
import shutil
import glob
import time
# Inport PostgreSQL
import psycopg2
import pandas as pd
import numpy as np
import json
import json5

from openpyxl.workbook import Workbook
# Configure pandas options
pd.options.mode.copy_on_write = True
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured


# Carga la clave
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Desencripta el archivo
with open("secret.enc", "rb") as enc_file:
    encrypted = enc_file.read()

# Cargo las variables secretos desde el archivo secret.enc
decrypted = fernet.decrypt(encrypted)
secret = json.loads(decrypted.decode())

# Función para obtener las variables secretas 
def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = f"La variable secreta:{secret_name} no existe"
        raise ImproperlyConfigured(msg)
   
# Cargo la configuracion desde el archivo config.json5
with open("config.json5", "r") as f:
    config = json5.loads(f.read())

# Función para obtener las variables de configuracion   
def get_config(config_name, configs=config):
    try:
        return configs[config_name]
    except:
        msg = "la variable %s no existe en el archivo de configuracion" % config_name
        raise ImproperlyConfigured(msg)
        
# Connect to your postgres DB
try:
    credenciales = {
        "dbname": get_secret("DB_NAME"),
        "user": get_secret("USER"),
        "password": get_secret("PASSWORD"),
        "host": "localhost",
        "port": '5432'
    }
    conn = psycopg2.connect(**credenciales)
    # Open a cursor to perform database operations
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Ocurrió un error de conexion con la base de datos PostgreSQL: ", e)
# Obtener los resultados
cur.execute(
    'SELECT id, datatime_db, state, tag, value, unit FROM django_schema.mediciones_measurementsdatafloat')

# Convertir a DataFrame
rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=columns)

# Cerrar la conexion
conn.commit()
conn.close()

# Mostrar los primeros registros
print(df.head())

# Elimina la zona horaria de la columna 'datatime_db'
df['datatime_db'] = pd.to_datetime(df['datatime_db']).dt.tz_localize(None)

# Guardar en un archivo Excel
df.to_excel("mediciones.xlsx", index=False)

# Esperar 5 segundos luego reslizar una copia del archivo a la carpeta de Google Drive
time.sleep(5)

# Carpeta origen y destino
#origen = r"C:\Users\Administrator\Documents\Repo_project\Python"
#destino = r"G:\My Drive\CompartidaNubeGoogleDrive"
origen = get_config("ORIGEN_EXCEL")
destino = get_config("DESTINO_EXCEL")
# Buscar todos los archivos que coincidan con el patrón
archivos = glob.glob(os.path.join(origen, "mediciones*.xlsx"))

# Copiar cada archivo al destino
for archivo in archivos:
    try:
        shutil.copy2(archivo, destino)  # copy2 preserva metadata (similar a /K en xcopy)
        print(f"Copiado: {archivo} -> {destino}")
    except Exception as e:
        print(f"Error copiando {archivo}: {e}")
        