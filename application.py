from PyQt5.QtWidgets import *
import sys
import main_window as run

app = QApplication(sys.argv)
main_window = run.MainWindow()
main_window.show()

app.exec_()
