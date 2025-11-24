# 1. Import of libraries
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QFile, QTimer
import readDB

# 2. Main form class definition and functions for reading data from DB
class mainFormReadDB(QDialog):
    def __init__(self):
        super().__init__()  # Inicializa QDialog correctamente
        self.ui = QUiLoader().load(QFile("main_window.ui"))
        self.ui.btnRead.clicked.connect(self.read)
# 2. Main form class definition and functions for reading data from DB
# class mainFormReadDB():
#     def __init__(self):
#         super(mainFormReadDB, self).__init__()
#         self.ui = QUiLoader().load(QFile("main_window.ui"))
#         self.ui.btnRead.clicked.connect(self.read)

        # 🚀 Crear un temporizador que refresque cada 5 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.read)   # cada vez que se cumpla el tiempo, llama a read()
        self.timer.start(5000)                  # intervalo en milisegundos (5000 ms = 5 segundos)

    def read(self):
        # 2.2.1 get data by running readDB function in readDB.py
        datos = readDB.readDB()

        # 2.2.2 assign data to variables
        cpuType = datos[0]
        cpuStatus = datos[1]
        name = datos[2]
        value = datos[3]
        status = datos[4]

        # 2.2.3 CPU data
        self.ui.txtCpuType.setText("{}".format(cpuType))

        # 2.2.4 CPU status LED
        if cpuStatus == 'S7CpuStatusRun':
            self.ui.ledCpuStatus.setStyleSheet(
                u"background-color: rgb(0, 255, 0);border-radius:15px;")
        else:
            self.ui.ledCpuStatus.setStyleSheet(
                u"background-color: rgb(255, 0, 0);border-radius:15px;")

        # 2.2 DB data
        self.ui.txtName.setText("{}".format(name))
        self.ui.lcdValue.setProperty("intValue", value)
        if status is True:
            self.ui.ledStatus.setStyleSheet(
                u"background-color: rgb(0, 255, 0);border-radius:30px;")
        else:
            self.ui.ledStatus.setStyleSheet(
                u"background-color: rgb(255, 0, 0);border-radius:30px;")

# 3. Main program loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = mainFormReadDB()
    myapp.ui.show()
    sys.exit(app.exec())