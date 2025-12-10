'''
@autor: Jorge Garcia
Created on 11/15/2025
'''
# Programa para crear una ventana emergente con parámetros personalizables

# Importo las Librerias
from tkinter import *
import os


# Función para crear una ventana con parámetros personalizables
def crear_ventana(titulo_ventana, texto_label, color_fondo, color_label, tamano_ventana):
    root = Tk()
    root.geometry(tamano_ventana)  # Tamaño de la ventana
    root.resizable(True, True) # Permitir redimensionamiento

    # Ruta absoluta al icono
    icon_path = os.path.join(os.path.dirname(__file__), "icono1.ico")
    root.iconbitmap(icon_path) # Cambiar el icono

    # Título de la ventana
    root.title(titulo_ventana)

    # Fondo de la ventana
    root.config(bg=color_fondo)

    # Frame centrado con color de fondo
    frm = Frame(root, bg=color_fondo)
    frm.pack(expand=True)

    # Label centrado
    label = Label(frm, text=texto_label,
                  font=('Times', 20, 'bold italic'),
                  fg="blue", bg=color_label, 
                  wraplength=350, # ancho máximo antes de saltar de línea
                  justify=CENTER) # alineación del texto
    label.pack(pady=20, expand=True) # Espaciado vertical y expansión
    
    # Botón centrado
    btn = Button(frm,
             text="Quit",
             command=root.destroy,
             bg="gray",
             fg="black",
             font=('Times', 16, 'bold'))
    btn.pack(pady=10) # Espaciado vertical
    # Metodo cerrar ventana
    def cerrar():
        root.destroy()
    # Espera un tiempo luego ejecuta "cerrar"    
    #root.after(5000, cerrar)  # Cierra la ventana después de 5000 ms (5 segundos)    
    root.mainloop()


# Ejemplo de uso
if __name__ == "__main__":
    crear_ventana(
        titulo_ventana="WARNING - ALERTA USO DISCO",
        texto_label="[WARNING] ALERTA: El uso del disco supera el umbral definido del : 80 %",
        color_fondo="yellow",
        color_label="yellow",
        tamano_ventana="500x200"
    )