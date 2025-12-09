'''
@autor: Jorge Garcia
Created on 11/15/2025
'''
# Programa que crea un archivo Excel con los datos leidos de un PLC S7-1500

# Los datos estan almacenados en una base de datos PostgreSQL
import os
import socket
import subprocess
import shutil
import glob
import time
#PostgreSQL
import psycopg2
import pandas as pd
import numpy as np
import json
import json5

# Libreria para crear archivos Excel
from openpyxl.workbook import Workbook
# Configure pandas options
pd.options.mode.copy_on_write = True
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured

# Nombre y Serial de los Disco de la Maquina fisica/Virtual
# Nombre de la máquina
hostname = socket.gethostname() # En Linux y Windows
#print("Nombre de la máquina:", hostname)
# Obtener el nombre del host usando socket como alternativa
result = subprocess.run(
    ["wmic", "diskdrive", "get", "serialnumber"],
    capture_output=True,
    text=True
)
# Divide la salida en líneas, elimina espacios vacíos y toma la última línea
lines = result.stdout.strip().splitlines()

# La primera línea es el título, la segunda (o siguientes) son los seriales
serials = [line.strip() for line in lines if line.strip() and line.strip() != "SerialNumber"]

# Si hay más de un disco, tendrás varios seriales en la lista
serial_number = serials[0]  # primer disco
#print("Serial limpio:", serial_number)
    
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
        msg = f"\n La variable secreta:{secret_name} no existe"
        raise ImproperlyConfigured(msg)
   
# Cargo la configuracion desde el archivo config.json5
with open("config.json5", "r") as f:
    config = json5.loads(f.read())

# Función para obtener las variables de configuracion   
def get_config(config_name, configs=config):
    try:
        return configs[config_name]
    except:
        msg = "\n la variable %s no existe en el archivo de configuracion" % config_name
        raise ImproperlyConfigured(msg)
    
# Verifico el nombre de la maquina y el serial 
if hostname != get_secret("HOST_NAME") or serial_number != get_secret("SERIAL_NUMBER"):
    print("\n Acceso denegado. Favor hablar con soperte tecnico.")
    exit(1) # Salir del programa si no coincide el nombre o serial
print('\n -----------------------------------------')    
print("\n Acceso concedido. Bienvenido al sistema. Espere mientras se crea el archivo de Excel...")
            
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
    print("\n [OK] Se realizo la conexion con la base de datos PostgreSQL: ", credenciales["dbname"])
except psycopg2.Error as e:
    print("\n Ocurrió un error de conexion con la base de datos PostgreSQL: ", e)
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
# print('\n -----------------------------------------') 
# print(df.head())
# print('\n -----------------------------------------')
 
# Elimina la zona horaria de la columna 'datatime_db'
df['datatime_db'] = pd.to_datetime(df['datatime_db']).dt.tz_localize(None)

# Guardar en un archivo Excel
name_excel = get_config("NAME_EXCEL")
df.to_excel(name_excel, index=False)

print(f"\n [OK] Archivo Excel '{name_excel}' creado exitosamente.")

# Esperar 5 segundos luego reslizar una copia del archivo a la carpeta de Google Drive
time.sleep(5)

# Carpeta origen y destino
origen = get_config("ORIGEN_EXCEL")
destino = get_config("DESTINO_EXCEL")
# Buscar todos los archivos que coincidan con el patrón
archivos = glob.glob(os.path.join(origen, name_excel))
print('\n -----------------------------------------') 
# Copiar cada archivo al destino
for archivo in archivos:
    try:
        shutil.copy2(archivo, destino)  # copy2 preserva metadata (similar a /K en xcopy)
        print(f"Copiado: {archivo} -> {destino}")
    except Exception as e:
        print(f"Error copiando {archivo}: {e}")
print('\n -----------------------------------------')          