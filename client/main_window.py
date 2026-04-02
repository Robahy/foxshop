from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database import ServerManager
from pages import MainPage, FactorPage, ProductManagementPage, PersonnelManagerPage
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.changer_page = QStackedWidget()
        self.changer_page.setStyleSheet("background: #1e1e1e")

        self.foxapi = ServerManager()
        
        # Pages
        main_page              = MainPage(self.changer_page, self.foxapi) # Page 0
        factor_page            = FactorPage(self.changer_page, self.foxapi) # Page 1
        product_manager_page   = ProductManagementPage(self.changer_page, self.foxapi) # Page 2
        personnel_manager_page = PersonnelManagerPage(self.changer_page, self.foxapi) # Page 3

        # Add Pages
        self.changer_page.addWidget(main_page)
        self.changer_page.addWidget(factor_page)
        self.changer_page.addWidget(product_manager_page)
        self.changer_page.addWidget(personnel_manager_page)


        self.setCentralWidget(self.changer_page)
        self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())