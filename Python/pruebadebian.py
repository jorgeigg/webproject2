import sys
import termios
import tty
import time

def getch():
    """Lee una tecla sin necesidad de Enter (solo Linux/Unix)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)              # modo lectura cruda
        ch = sys.stdin.read(1)      # lee un solo carácter
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Bucle de lectura continua
while True:
    print("Tiempo de espera.")
    time.sleep(5)

    # Capturo una tecla
    tecla = getch()
    if tecla.lower() == 'q':
        print("\nPrograma terminado por el usuario.")
        break