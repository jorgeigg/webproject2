import psycopg2
import shutil
import os
from psycopg2 import sql

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


def check_disk_usage(path="/", threshold=0.8):
    """Verifica el uso del disco en la ruta indicada"""
    total, used, free = shutil.disk_usage(path)
    usage_percent = used / total
    return total, used, free, usage_percent, usage_percent > threshold


def pretty_size(size_bytes):
    """Convierte bytes a formato legible"""
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


if __name__ == "__main__":
    # Configuración de conexión
    dbname="mediciones_db"
    user="usermedapp"
    password="#Siemens12345"
    host="localhost"  # Cambia si tu servidor está en otra máquina
    port=5432

    # Ruta del disco donde está PostgreSQL (Windows: C:\\, Linux: /var/lib/postgresql o /)
    disk_path = "/" if os.name != "nt" else "C:\\"

    # Obtener tamaños
    db_size, tables = get_db_and_table_sizes(dbname, user, password, host, port)
    total, used, free, usage_percent, alert = check_disk_usage(disk_path)

    print(f"Tamaño de la base '{dbname}': {pretty_size(db_size)}")
    print("\nTamaños de tablas:")
    for table_name, total_size in tables:
        print(f"- {table_name}: {pretty_size(total_size)}")

    print("\nEstado del disco:")
    print(f"Total: {pretty_size(total)} | Usado: {pretty_size(used)} | Libre: {pretty_size(free)}")
    print(f"Uso: {usage_percent*100:.2f}%")

    if alert:
        print("⚠️ ALERTA: El uso del disco supera el umbral definido.")