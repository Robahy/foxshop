import sys
from PyQt5.QtWidgets import QApplication
from pages.factor_main import FactorMain

app = QApplication(sys.argv)

window = FactorMain()
window.show()

app.exec_() # Start Fox Pos
# print(window.myfactor)