# Importo las Librerias
import os
import time
import ctypes
import snap7
import json
import json5
from snap7.util import *
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured

# Verifico la carga del snap7
try:
    # Activo el Driver de comunicacion
    plc = snap7.client.Client()
    print("✅ La libreria Snap7 cargado correctamente.")   
except Exception as e:
    msg = "✅ La libreria Snap7 no cargado correctamente: %s" % str(e)
    raise ImproperlyConfigured(msg)


# Verifico la conexion con el PLC
# Me conecto con el PLC
plc.connect('192.168.0.1', 0, 1)
print("✅ Conectado al PLC.")
# Leo la base de datos del PLC y lo carga en una variable
db = plc.db_read(302, 0, 1032)
# leo el dato Valor por rango de byte y le aplico un formato
state1 = int.from_bytes(db[256:258], byteorder='big')
print(f'STATE1: {state1}')
# leo el dato Valor por rango de byte y le aplico un formato
state2 = int.from_bytes(db[514:516], byteorder='big')
print(f'STATE2: {state2}')

STATE_VALUE_INI = 256
STATE_VALUE_END = 258
# valor_a_escribir = 32767
valor_a_escribir = 2
# Convertir a bytes
data = valor_a_escribir.to_bytes(STATE_VALUE_END - STATE_VALUE_INI, byteorder='big')

# Escribir en el PLC
plc.db_write(302, STATE_VALUE_INI, data)
# Leo la base de datos del PLC y lo carga en una variable
db = plc.db_read(302, 0, 1032)
# leo el dato Valor por rango de byte y le aplico un formato
state = int.from_bytes(db[STATE_VALUE_INI:STATE_VALUE_END], byteorder='big')
print(f'STATE2: {state}')

# Desconecto del PLC
plc.disconnect()
