# Importo las Librerias
import os
import ctypes
import snap7
import json
import json5
from snap7.common import Snap7Library
from django.core.exceptions import ImproperlyConfigured

# 
with open("config.json5", "r") as f:
    config = json5.load(f)

with open("secret.json") as f:
    secret = json.loads(f.read())
    
def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)

# Cargar snap7.dll manualmente como stdcall (requerido en Windows)
dll_path = os.path.abspath("snap7.dll")
snap7.common.library = Snap7Library(dll_path).cdll


# Declaro las variables de comunicacion
IP = config["IP"]
RACK = config["RACK"]
SLOT = config["SLOT"]
PRODUCT_NAME_INI = 0
PRODUCT_NAME_END = 256
PRODUCT_VALUE_INI = 256
PRODUCT_VALUE_END = 258
PRODUCT_STATUS = 258
DB_END = 258.1

# Declaro las variables de conexion con la DB del PLC
DB_NUMBER = 3
START_ADDRESS = 0
SIZE = 259

try: 
    # Activo el Driver de comunicacion  
    plc = snap7.client.Client()
    print("✅ Snap7 cargado correctamente.")
    # Me conecto con el PLC
    plc.connect(IP, RACK, SLOT)
    # Verifico si estoy conectado
    if plc.get_connected():
        print("✅ Esta Conectado al PLC")
        # Leo la base de datos del PLC y lo carga en una variable
        db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
        # Leo el dato String por rango de byte y le aplico un formato
        # Para PLCs Siemens, lo más seguro es usar 'latin1' o 'ascii' si sabes 
        # que el texto no tiene acentos ni símbolos especiales. 'utf-8' es más estricto y 
        # puede fallar con datos binarios o inicializados con 0xFE, 0xFF, etc.
        #product_name = db[0:256].decode('UTF-8').strip('\x00')
        #product_name = db[0:256].decode('latin1').strip('\x00')
        product_name = db[PRODUCT_NAME_INI:PRODUCT_NAME_END].decode('utf-8', errors='ignore').strip('\x00')
        print(f'PRODUCT NAME: {product_name}')
        # leo el dato Valor por rango de byte y le aplico un formato
        product_value = int.from_bytes(db[PRODUCT_VALUE_INI:PRODUCT_VALUE_END], byteorder='big')
        print(f'PRODUCT VALUE: {product_value}')
        # leo el dato Booliano por rango de byte y le aplica un formato
        product_status = bool(db[PRODUCT_STATUS])
        print(f'PRODUCT STATUS: {product_status}')       
    else:
        print("❌ No esta conectado al PLC")
    # Me desconecto
    plc.disconnect()
except Exception as e:
    print("❌ Error al cargar Snap7 Client: ", e)