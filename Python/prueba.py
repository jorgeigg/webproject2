# Nombre y Serial de los Disco de la Maquina fisica/Virtual
import os
import socket
import subprocess

# Nombre de la máquina
hostname = os.environ.get("COMPUTERNAME")  # En Windows
print("Nombre de la máquina:", hostname)

hostname = socket.gethostname()
print("Nombre de la máquina:", hostname)


# Ejecuta el comando WMIC
result = subprocess.run(
    ["wmic", "diskdrive", "get", "serialnumber"],
    capture_output=True,
    text=True
)

# Divide la salida en líneas, elimina espacios vacíos y toma la última línea
lines = result.stdout.strip().splitlines()

# La primera línea es el título, la segunda (o siguientes) son los seriales
serials = [line.strip() for line in lines if line.strip() and line.strip() != "SerialNumber"]

# Si hay más de un disco, tendrás varios seriales en la lista
serial_number = serials[0]  # primer disco
print("Serial limpio:", serial_number)