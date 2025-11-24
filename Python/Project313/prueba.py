import PySide6
import sys
import snap7
print(PySide6.__version__)
print(sys.version)
print(sys.executable)

# 1. PLC connection definition
IP = '192.168.0.1'
RACK = 0
SLOT = 1

# 1.1 PLC connection via snap7 client module
plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

# 2. Read PLC data
plc_info = plc.get_cpu_info()
plc_Type = plc_info.ModuleTypeName.decode('UTF-8').strip('\x00')
print(f'Module Type: {plc_info.ModuleTypeName}')
plc_state = plc.get_cpu_state()
print(f'State:{plc_state}')

# 3. Point DB and read data
db1 = plc.db_read(302, 0, 258)
db2 = plc.db_read(303, 0, 258)
product_name = db1[2:256].decode('UTF-8').strip('\x00')
print(f'PRODUCT NAME: {product_name}')
product_value = int.from_bytes(db1[256:258], byteorder='big')
print(f'PRODUCT VALUE: {product_value}')
bool_name = db2[2:256].decode('UTF-8').strip('\x00')
print(f'BOOL NAME: {bool_name}')
product_status = bool(db2[256])
print(f'PRODUCT STATUS: {product_status}')