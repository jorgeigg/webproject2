'''
@autor: Jorge Garcia
Created on 11/15/2025
'''

# Programa que elimina datos antiguos de una tabla PostgreSQL basada en una condición de fecha

# Importo las Librerias
import psycopg2
import json

from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured
from datetime import date, timedelta

todays_date = date.today() # current time 'yy-mm-dd' UTC
#print("Current date: ", todays_date)


# Carga la clave
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key) # Create the Fernet instance

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
    
# Función para eliminar datos antiguos de una tabla basada en una condición de fecha
def delete_data_table(data_day):
    # Conectar a la base de datos
    conn = psycopg2.connect(
        dbname=get_secret("DB_NAME"),
        user=get_secret("USER"),
        password=get_secret("PASSWORD"),
        host="localhost",
        port=5432
    )
    # Crear un cursor
    cur = conn.cursor()
    
    # Calculo el numero de dias
    var_dia = timedelta(days=data_day)
    deltatime = todays_date - var_dia
    #print("DELTATIME: ", deltatime)
    
    # Tamaño de cada tabla
    # query = """
    # SELECT * FROM django_schema.mediciones_measurementsdatafloat
    # WHERE datatime_db < '%s'
    # ORDER BY id ASC LIMIT 10;
    # """ % (deltatime)
    query = """
    DELETE FROM django_schema.mediciones_measurementsdatafloat
	WHERE datatime_db < '%s';
    """ % (deltatime)
    
    # Ejecutar la consulta
    cur.execute(query)
    # Obtener los resultados
    deleted_rows = cur.rowcount  # ✅ cantidad de filas eliminadas
    #print(f"Deleted rows: {deleted_rows}")
       
    # Cerrar el cursor
    cur.close()
    # Cerrar la conexion a la base de datos
    conn.close()
    #result = cur.fetchall()
    # Imprimo los resultados
    # for i in result:
    #     print(i)        
    return deleted_rows

# Ejemplo de uso
# if __name__ == "__main__":
#     delete_data_table(
#         data_day=365
#     )