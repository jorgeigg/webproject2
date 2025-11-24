# Importo las Librerias
import os
import time
import snap7
import json
import json5
import keyboard
import datetime
#PostgreSQL
import psycopg2
from snap7.util import *
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured
from datetime import date

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
        
# Declaro las variables de comunicacion
#data_today = date.today()
IP = get_config("IP")
RACK = get_config("RACK")
SLOT = get_config("SLOT")
WAITING_TIME = get_config("WAITING_TIME")
DB_NUMBER1 = get_config("DB_NUMBER1")
START_ADDRESS1 = get_config("START_ADDRESS1")
SIZE1 = get_config("SIZE1")
STATE1_NAME_INI = get_config("STATE1_NAME_INI")
STATE1_NAME_END = get_config("STATE1_NAME_END")
STATE1_VALUE_INI = get_config("STATE1_VALUE_INI")
STATE1_VALUE_END = get_config("STATE1_VALUE_END")
STATE2_NAME_INI = get_config("STATE2_NAME_INI")
STATE2_NAME_END = get_config("STATE2_NAME_END")
STATE2_VALUE_INI = get_config("STATE2_VALUE_INI")
STATE2_VALUE_END = get_config("STATE2_VALUE_END")
DB_NUMBER2 = get_config("DB_NUMBER2")
START_ADDRESS2 = get_config("START_ADDRESS2")
SIZE2 = get_config("SIZE2")
MEAS_NAME_INI = get_config("MEAS_NAME_INI")
MEAS_NAME_END = get_config("MEAS_NAME_END")
MEAS_VALUE_INI = get_config("MEAS_VALUE_INI")
MEAS_VALUE_END = get_config("MEAS_VALUE_END")
MEAS_UNIT_INI = get_config("MEAS_UNIT_INI")
MEAS_UNIT_END = get_config("MEAS_UNIT_END")
CTTE_ADDRESS = get_config("CTTE_ADDRESS")

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
    # Open a cursor to perform database operations
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Ocurrió un error de conexion con la base de datos PostgreSQL: ", e)

#print(IP,RACK,SLOT)

# Verifico la carga del snap7
try:
    # Activo el Driver de comunicacion
    plc = snap7.client.Client()
    print("✅ La libreria Snap7 cargado correctamente.")   
except Exception as e:
    msg = "✅ La libreria Snap7 no cargado correctamente: %s" % str(e)
    raise ImproperlyConfigured(msg)

# Verifico la conexion con el PLC
try:
    # Me conecto con el PLC
    plc.connect(IP, RACK, SLOT)
        # Verifico si estoy conectado
    if plc.get_connected():
        print("✅ Esta Conectado al PLC")
        # Leo la informacion general del PLC
        # plc_info = plc.get_cpu_info()
        # print('------------------------')
        # print(f"MODULE TYPE: {plc_info.ModuleTypeName}")
        # print(f"COPYRIGHT: {plc_info.Copyright}")
        # print('------------------------')

        # Bucle de lectura continua
        while True:
            # Verifico que no se ha presionado la tecla 'q'
            if keyboard.is_pressed('q'):
                print("\nPrograma terminado por el usuario.")
                break

            # Declaro variables
            colu0 = list()
            colu1 = list() 
            colu2 = list()
            colu3 = list()
            ctte = 0
            
            print("Fecha y hora actual:", datetime.datetime.now())
            
            # Leo la base de datos del PLC y lo carga en una variable
            db1 = plc.db_read(DB_NUMBER1, START_ADDRESS1, SIZE1)

            # leo el dato Valor por rango de byte y le aplico un formato
            state1 = int.from_bytes(db1[STATE1_VALUE_INI:STATE1_VALUE_END], byteorder='big')
            print(f'STATE1: {state1}')
            state2 = int.from_bytes(db1[STATE2_VALUE_INI:STATE2_VALUE_END], byteorder='big')
            #print(f'STATE2: {state2}')
            # Convertir a bytes
            data = state1.to_bytes(STATE2_VALUE_END - STATE2_VALUE_INI, byteorder='big')
            # Escribir en el PLC
            plc.db_write(DB_NUMBER1, STATE2_VALUE_INI, data)
            
            # Si el estado es 0, salgo del bucle
            if state1 >= 0:               
                # Leo la base de datos del PLC y lo carga en una variable
                db2 = plc.db_read(DB_NUMBER2, START_ADDRESS2, SIZE2) 
           
            # Bucle de lectura de datos del PLC tipo  Float            
            while True:                 
                # Si el estado es 0, salgo del bucle
                if state1 == 0:
                    break
                # Leo el nombre de la medida
                meas_name = db2[MEAS_NAME_INI+ctte:MEAS_NAME_END+ctte].decode('utf-8', errors='ignore').strip('\x00')
                #print(f'MEAS NAME: {meas_name}')
                
                # Si el nombre de la medida es vacío, salgo del bucle
                if meas_name == '' or meas_name is None:
                    break
                # Leo el valor de la medida                                
                dbf = plc.db_read(DB_NUMBER2,MEAS_VALUE_INI+ctte,4)
                meas_value = round(get_real(dbf, 0), 2)
                #print(f'MEAS VALUE: {meas_value}')
                # Leo la unidad de la medida
                meas_unit = db2[MEAS_UNIT_INI+ctte:MEAS_UNIT_END+ctte].decode('utf-8', errors='ignore').strip('\x00')
                #print(f'MEAS UNIT: {meas_unit}')
                
                # Crear el texto del Query
                query = '''
                INSERT INTO django_schema.mediciones_measurementsdatafloat(
                    datatime_db, state, tag, value, unit)
                    VALUES ( \'%s\', %s, \'%s\', %s, \'%s\');
                ''' % (datetime.datetime.now(), state1, meas_name, meas_value, meas_unit)
                # Ejecutar una consulta
                cur.execute(query)
                
                # Incremento el contador                
                ctte = ctte + CTTE_ADDRESS


            # Esperar segundos antes de la siguiente lectura
            time.sleep(WAITING_TIME)
                               
except Exception as e:
    msg = "✅ No esta Conectado al PLC: %s" % str(e)
    raise ImproperlyConfigured(msg)

# Desconecto del PLC
plc.disconnect()
# Cerrar la conexion a la base de datos
conn.commit()
conn.close()
