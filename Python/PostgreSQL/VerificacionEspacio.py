# Instalar pip install psycopg2-binary o psycopg2
# Usuario con permisos de lectura en las tablas.

import psycopg2
from psycopg2 import sql

def get_db_and_table_sizes(dbname, user, password, host="localhost", port=5432):
    try:
        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        # Tamaño total de la base
        cur.execute(sql.SQL("SELECT pg_size_pretty(pg_database_size(%s));"), [dbname])
        db_size = cur.fetchone()[0]
        print(f"Tamaño total de la base '{dbname}': {db_size}")

        # Tamaño de cada tabla
        query = """
        SELECT relname AS table_name,
               pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
               pg_size_pretty(pg_relation_size(relid)) AS data_size,
               pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS index_size
        FROM pg_catalog.pg_statio_user_tables
        ORDER BY pg_total_relation_size(relid) DESC;
        """
        cur.execute(query)
        tables = cur.fetchall()

        print("\nTamaños de tablas:")
        for table_name, total_size, data_size, index_size in tables:
            print(f"- {table_name}: total={total_size}, datos={data_size}, índices={index_size}")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error al conectar o consultar:", e)


# Ejemplo de uso
if __name__ == "__main__":
    get_db_and_table_sizes(
        dbname="mediciones_db",
        user="usermedapp",
        password="#Siemens12345",
        host="localhost",  # Cambia si tu servidor está en otra máquina
        port=5432
    )