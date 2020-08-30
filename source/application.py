import sys
import os


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root)
sys.path.append(root)

from PyQt5.QtWidgets import *
import frontend.main_window as run

app = QApplication(sys.argv)
main_window = run.MainWindow()
main_window.show()

app.exec_()
