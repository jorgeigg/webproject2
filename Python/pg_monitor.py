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
from django.core.exceptions import ImproperlyConfigured
from psycopg2 import sql

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