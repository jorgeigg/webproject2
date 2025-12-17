'''
@autor: Jorge Garcia
Created on 11/15/2025
'''
# Programa que se monitorea el tamaño de la base de datos PostgreSQL y el uso del disco

# Importo las Librerias
import psycopg2
import shutil
import os
import json5
import json
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured
from psycopg2 import sql

# Carga la clave
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "secret.key"), "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key) # Create the Fernet instance

# Desencripta el archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "secret.enc"), "rb") as enc_file:
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "config.json5"), "r") as f:
    config = json5.loads(f.read())

# Función para obtener las variables de configuracion   
def get_config(config_name, configs=config):
    try:
        return configs[config_name]
    except:
        msg = "\n la variable %s no existe en el archivo de configuracion" % config_name
        raise ImproperlyConfigured(msg)

# Función para obtener el tamaño de la base de datos y de las tablas
def get_db_and_table_sizes(dbname, user, password, host="localhost", port=5432):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()

    # Tamaño total de la base
    cur.execute(sql.SQL("SELECT pg_database_size(%s);"), [dbname])
    db_size_bytes = cur.fetchone()[0]

    # Tamaño de cada tabla
    query = """
    SELECT relname AS table_name,
           pg_total_relation_size(relid) AS total_size
    FROM pg_catalog.pg_statio_user_tables
    ORDER BY pg_total_relation_size(relid) DESC;
    """
    cur.execute(query)
    tables = cur.fetchall()

    cur.close()
    conn.close()

    return db_size_bytes, tables

# Verifica el uso del disco (threshold=0.8 por defecto)
def check_disk_usage(path="/", threshold = get_config("ALERT_DISK")):
    """Verifica el uso del disco en la ruta indicada"""
    total, used, free = shutil.disk_usage(path)
    usage_percent = used / total
    return total, used, free, usage_percent, usage_percent > threshold

# Convierte bytes a formato legible
def pretty_size(size_bytes):
    """Convierte bytes a formato legible"""
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

# Ejemplo de uso
# if __name__ == "__main__":   
#     dbname = get_secret("DB_NAME")
#     user = get_secret("USER")
#     password = get_secret("PASSWORD")
    
#     db_size, tables = get_db_and_table_sizes(dbname, user, password)
#     print(f"Tamaño total de la base de datos '{dbname}': {pretty_size(db_size)}")
#     print("Tamaños de las tablas:")
#     for table_name, size in tables:
#         print(f" - {table_name}: {pretty_size(size)}")
    
#     total, used, free, usage_percent, alert = check_disk_usage("/", get_config("ALERT_DISK"))
#     print(f"\nUso del disco en '/':")
#     print(f" - Total: {pretty_size(total)}")
#     print(f" - Usado: {pretty_size(used)}")
#     print(f" - Libre: {pretty_size(free)}")
#     print(f" - Porcentaje usado: {usage_percent*100:.2f}%")
#     if alert:
#         print("¡Alerta! El uso del disco ha superado el umbral establecido.")
