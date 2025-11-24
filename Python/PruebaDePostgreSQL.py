# DATOS
# Consulta Basica
#PostgreSQL
import psycopg2
from datetime import date
# Connect to your postgres DB
try:
    credenciales = {
        "dbname": "mediciones_db",
        "user": "usermedapp",
        "password": "#Siemens12345",
        "host": "localhost",
        "port": '5432'
    }
    conn = psycopg2.connect(**credenciales)
except psycopg2.Error as e:
    print("Ocurrió un error de conexion con la base de datos PostgreSQL: ", e)

# Open a cursor to perform database operations
cur = conn.cursor()
var0 = date.today()
var1 = 1
var2 = 'TAG1'
var3 = 23.5
vat4 = 'm3/h'
# Crear el texto del Query
query = '''
INSERT INTO django_schema.mediciones_measurementsdatafloat(
	datatime_db, state, tag, value, unit)
	VALUES ( \'%s\', %s, \'%s\', %s, \'%s\');
''' % (var0, var1, var2, var3, vat4)
# Ejecutar una consulta
cur.execute(query)
# Obtener los resultados
cur.execute(
    'SELECT id, datatime_db, state, tag, value, unit FROM django_schema.mediciones_measurementsdatafloat')
for i in cur:
    print(i)

conn.commit()
conn.close()