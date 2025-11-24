# --------------------------------------------------------------------------------------
# | Py module: main.py                                                                 |
# | Author: David García Rincón                                                        |
# | Date: 20210719                                                                     |
# | Version: 1.0 x64                                                                   |
# | Purpose: free software for testing and developing. Right working is not guarantied |
# --------------------------------------------------------------------------------------
# |                                        description                                 |
# --------------------------------------------------------------------------------------
# | This module is opening the ui form in #1                                           |
# | Generate the proccedure of the button read data in #2 calling the function readDB  |
# | included in module readDB.py mandatory                                             |
# --------------------------------------------------------------------------------------
# TODO: Comandos importantes para el desarrollo de la aplicación
# # C:\Users\Administrator\Documents\Repo_project\Python\venv313\Scripts\Activate.ps1 (Activa el entorno virtual)
# # python .\prueba.py (Ejecuta un prog.)

# 1. Import of libraries
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QFile
import readDB

# 2. Main form class definition and functions for reading data from DB
class mainFormReadDB():
    # 2.1 Declaration of the main form and call functions
    def __init__(self):
        super(mainFormReadDB, self).__init__() # Call to the parent class constructor
        #super().__init__() # JORGE: Call to the parent class constructor
        self.ui = QUiLoader().load(QFile("main_window.ui")) # Load the .ui file
        # Connect the btnRead button to the read function
        self.ui.btnRead.clicked.connect(self.read) # when clicked, call self.read

    # 2.2 ReadDB function when click on ReadDB button
    def read(self):
        # 2.2.1 get data by running readDB function in readDB.py
        #readDB.readDB() # OJO esta linea NO ES NECESARIA
         # 2.2.2 assign data to variables
        datos = readDB.readDB()
        cpuType = datos[0]
        cpuStatus = datos[1]
        name = datos[2]
        value = datos[3]
        status = datos[4]

        # 2.2.3 CPU data 
        self.ui.txtCpuType.setText("{}".format(cpuType))  
        # 2.2.4 CPU status LED
        if cpuStatus == 'S7CpuStatusRun':
            self.ui.ledCpuStatus.setStyleSheet(u"background-color: rgb(0, 255, 0);border-radius:15px;")
        else:
            self.ui.ledCpuStatus.setStyleSheet(u"background-color: rgb(255, 0, 0);border-radius:15px;")

        # 2.2 DB data
        self.ui.txtName.setText("{}".format(name))
        self.ui.lcdValue.setProperty("intValue", value)
        if status == True:
            self.ui.ledStatus.setStyleSheet(
                u"background-color: rgb(0, 255, 0);border-radius:30px;")
        else:
            self.ui.ledStatus.setStyleSheet(
                u"background-color: rgb(255, 0, 0);border-radius:30px;")

# 3. Main program loop
if __name__ == "__main__": # Main program check, ejecuted when the module is run directly
    app = QApplication(sys.argv) # QApplication instance creation, sys.argv command line arguments
    myapp = mainFormReadDB() # mainFormReadDB class instance creation, equivalent to main window
    myapp.ui.show() # Show the main form, making it visible. open the window
    sys.exit(app.exec_()) # Execute the main loop and exit the program
