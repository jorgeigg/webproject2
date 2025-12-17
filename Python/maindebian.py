'''
@autor: Jorge Garcia
Created on 11/15/2025
'''
# Programa que se comunica con un PLC S7-1500/Siemens y almacena los datos en una base de datos PostgreSQL

# Importo las Librerias
import os
import socket
import subprocess
import snap7
import json
import json5
#import keyboard
import datetime
#PostgreSQL
import psycopg2
from snap7.util import *
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured


from pg_monitor import get_db_and_table_sizes, check_disk_usage, pretty_size
from pop_up_window import crear_ventana
from pg_delete_data import delete_data_table
from pynput import keyboard

# Funcion para leer una tecla sin necesidad de presionar Enter (solo Linux/Unix).
pressed_q = False
def on_press(key):
    global pressed_q
    try:
        if key.char == 'q':
            pressed_q = True
    except:
        pass
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Nombre y Serial de los Disco de la Maquina fisica/Virtual
# Nombre de la máquina
hostname = socket.gethostname() # En Linux y Windows
#print("Nombre de la máquina:", hostname)

# Alternativa para Linux usando hdparm para obtener el serial del disco
def get_disk_serial_linux(device="/dev/sda"):
    try:
        result = subprocess.run(
            ["sudo", "hdparm", "-I", device],
            capture_output=True,
            text=True
        )
        for line in result.stdout.splitlines():
            if "Serial Number" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        return f"Error: {e}"

serial_number = get_disk_serial_linux("/dev/sda")
#print("Número de serie del disco:", serial_number)

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
        msg = f"La variable secreta:{secret_name} no existe"
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
        msg = "la variable %s no existe en el archivo de configuracion" % config_name
        raise ImproperlyConfigured(msg)

# Función principal para ejecutar el monitoreo del tamaño de la base de datos y uso del disco
def run_monitor(dbname, user, password, host="localhost", port=5432):
    # Ruta del disco donde está PostgreSQL
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
        print('\n -----------------------------------------')  
        print(f"\n [WARNING] ALERTA: El uso del disco supera el umbral definido del : {get_config('ALERT_DISK')*100}%")
        print('\n -----------------------------------------')
        crear_ventana(
        titulo_ventana="WARNING - ALERTA USO DISCO",
        texto_label=f"[WARNING] ALERTA: El uso del disco supera el umbral definido del : {get_config('ALERT_DISK')*100}%",
        color_fondo="yellow",
        color_label="yellow",
        color_texto_label= "blue",
        tamano_ventana="500x200"
        )
# Declaro las variables de comunicacion
# data_today = date.today()
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

# Verifico el nombre de la maquina y el serial 
if hostname != get_secret("HOST_NAME"):
    print('\n -----------------------------------------')  
    print("\n Acceso denegado. Favor hablar con soperte tecnico.")
    print('\n -----------------------------------------') 
    exit(1) # Salir del programa si no coincide el nombre o serial
print('\n -----------------------------------------')    
print("\n Acceso concedido. Bienvenido al sistema. Espere mientras se crea el archivo de Excel...")
print('\n -----------------------------------------')  
# Ejecuto el monitoreo del tamaño de la base de datos y uso del disco
# Aquí pasas solo los parámetros de conexión
run_monitor(
    dbname=get_secret("DB_NAME"),
    user=get_secret("USER"),
    password=get_secret("PASSWORD"),
    host="localhost",
    port=5432
)
# Elimino los datos antiguos de la base de datos
registro_eliminados = delete_data_table(get_config("RANGE_DAY_DEL"))
print('\n -----------------------------------------') 
print("\n Total de registros eliminados de la tabla: ", registro_eliminados)
print('\n -----------------------------------------') 
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
    print('\n -----------------------------------------')      
    print("\n [OK] Se realizo la conexion con la base de datos PostgreSQL: ", credenciales["dbname"])
    print('\n -----------------------------------------')  
except psycopg2.Error as e:
    print('\n -----------------------------------------')      
    print("\n Ocurrió un error de conexion con la base de datos PostgreSQL: ", e)
    print('\n -----------------------------------------')  

# Verficar el IP,RACK,SLOT    
#print(IP,RACK,SLOT)

# Verifico la carga del snap7
try:
    # Activo el Driver de comunicacion
    plc = snap7.client.Client()
    print('\n -----------------------------------------')    
    print("[OK] La libreria Snap7 cargado correctamente.")   
    print('\n -----------------------------------------')  
except Exception as e:
    msg = "[OK] La libreria Snap7 no cargado correctamente: %s" % str(e)
    raise ImproperlyConfigured(msg)

# Verifico la conexion con el PLC
try:
    # Me conecto con el PLC
    plc.connect(IP, RACK, SLOT)
    # Verifico si estoy conectado
    if plc.get_connected():
        print('\n -----------------------------------------')
        print("[OK] Esta Conectado al PLC")
        print('\n -----------------------------------------')
        # Leo la informacion general del PLC
        plc_info = plc.get_cpu_info()
        # print('------------------------')
        # print(f"MODULE TYPE: {plc_info.ModuleTypeName}")
        # print(f"COPYRIGHT: {plc_info.Copyright}")
        # print('------------------------')
        # print("Presiona 'q' para salir...")
        
        # Bucle de lectura continua
        while True:
            # Verifico que no se ha presionado la tecla 'q'
            # Capturo una tecla
            if pressed_q:
                print("\n -----------------------------------------")
                print(" Programa terminado por el usuario.")
                print(" -----------------------------------------\n")
                break
           
            # Declaro variables
            ctte = 0
            
            print("Fecha y hora actual:", datetime.datetime.now())
            
            # Leo la base de datos del PLC y lo carga en una variable
            db1 = plc.db_read(DB_NUMBER1, START_ADDRESS1, SIZE1)
            # leo el dato Valor por rango de byte y le aplico un formato
            state1 = int.from_bytes(db1[STATE1_VALUE_INI:STATE1_VALUE_END], byteorder='big')
            print(f'STATE1: {state1}')
            state2 = int.from_bytes(db1[STATE2_VALUE_INI:STATE2_VALUE_END], byteorder='big')
            print(f'STATE2: {state2}')
            
            # Si el estado es 0, salgo del bucle
            if state1 != 32767:               
                # Leo la base de  datos del PLC y lo carga en una variable
                db2 = plc.db_read(DB_NUMBER2, START_ADDRESS2, SIZE2)
                # print('!= 32767') 
            # Bucle de lectura de datos del PLC tipo  Float            
            while True:                
                # Si el estado es -1, salgo del bucle
                if state1 == 32767:
                    break
                # Leo el nombre de la medida
                meas_name = db2[MEAS_NAME_INI+ctte:MEAS_NAME_END+ctte].decode('utf-8', errors='ignore').strip('\x00')
                print(f'MEAS NAME: {meas_name}')
                 
                # Si el nombre de la medida es vacío, salgo del bucle
                if meas_name == '' or meas_name is None:
                    break 
                
                # Leo el valor de la medida                                
                dbf = plc.db_read(DB_NUMBER2,MEAS_VALUE_INI+ctte,4)
                meas_value = round(get_real(dbf, 0), 2)
                print(f'MEAS VALUE: {meas_value}')
                # Leo la unidad de la medida
                meas_unit = db2[MEAS_UNIT_INI+ctte:MEAS_UNIT_END+ctte].decode('utf-8', errors='ignore').strip('\x00')
                print(f'MEAS UNIT: {meas_unit}')

                
                # Open a cursor to perform database operations
                query = '''
                INSERT INTO mediciones_measurementsdatafloat(
                    datatime_db, state, tag, value, unit)
                    VALUES ( \'%s\', %s, \'%s\', %s, \'%s\');
                ''' % (datetime.datetime.now(), state1, meas_name, meas_value, meas_unit)
                # Open a cursor to perform database operations
                # Ejecutar una consulta
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                                 
                # Incremento el contador                
                ctte = ctte + CTTE_ADDRESS
                
            # Convertir a bytes
            data = state1.to_bytes(STATE2_VALUE_END - STATE2_VALUE_INI, byteorder='big')
            # Escribir en el PLC
            plc.db_write(DB_NUMBER1, STATE2_VALUE_INI, data)
            
            # Crear el texto del Query
            # query = '''
            # SELECT * FROM mediciones_measurementsdatafloat
            # ORDER BY id ASC LIMIT 10;
            # '''                 
            # Ejecutar una consulta
            # cur = conn.cursor()
            # cur.execute(query)
            # for i in cur:
            #     print(i)
            
            # Esperar segundos antes de la siguiente lectura
            #time.sleep(WAITING_TIME)                
except Exception as e:
    msg = "[OK] No esta Conectado al PLC: %s" % str(e)
    raise ImproperlyConfigured(msg)

# Desconecto del PLC
plc.disconnect()
# Cerrar la conexion a la base de datos
conn.close()