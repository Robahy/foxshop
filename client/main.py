import sys
from PyQt5.QtWidgets import QApplication, QDialog
from factor_main import FactorMain
from select_shoper_dialog import SelectShoperDialog

app = QApplication(sys.argv)

window = FactorMain()
window.show()

app.exec_() # Start Fox Pos
print(window.myfactor)