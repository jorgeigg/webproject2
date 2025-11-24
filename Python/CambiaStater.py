from snap7.client import Client

plc = Client()
plc.connect("192.168.0.1", 0, 1)

STATE2_VALUE_INI = 256
STATE2_VALUE_END = 258
valor_a_escribir = 0

# Convertir a bytes
data = valor_a_escribir.to_bytes(STATE2_VALUE_END - STATE2_VALUE_INI, byteorder='big')

# Escribir en el PLC
plc.db_write(302, STATE2_VALUE_INI, data)

print("✅ Valor escrito correctamente en el PLC.")