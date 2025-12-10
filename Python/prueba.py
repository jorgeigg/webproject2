# Interfaz Grafica
import os
from tkinter import *

raiz = Tk()
raiz.title("Primera Ventana") # Cambiar el nombre de la ventana
raiz.geometry("300x200") # Configurar tamaño

# Ruta absoluta al icono
icon_path = os.path.join(os.path.dirname(__file__), "yinyan.ico") 
raiz.iconbitmap(icon_path) # Cambiar el icono
raiz.config(bg="blue")  # Cambiar color de fondo
raiz.resizable(0, 0) # Deshabilitar redimensionamiento
raiz.mainloop() # Mantener ventana abierta

