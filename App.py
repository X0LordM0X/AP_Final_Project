import sys
from AppClass import App
from UIClasses import StartUpUI
from PyQt6.QtWidgets import QApplication

source = App()
app = QApplication(sys.argv)

window = StartUpUI(source)

window.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")