from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.factor_page import FactorPage
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.changer_page = QStackedWidget()
        self.showFullScreen()
        
        # Pages
        factor_page = FactorPage(self.changer_page) # Page 1

        # Add Pages
        self.changer_page.addWidget(factor_page)


        self.setCentralWidget(self.changer_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())