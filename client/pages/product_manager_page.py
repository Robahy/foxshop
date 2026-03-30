import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QPushButton, QHeaderView, QAbstractItemView, QTableWidgetItem
)
from PyQt5.QtCore import Qt

class ProductsTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "شماره سطر",
            "نام کالا",
            "قیمت کالا",
            "تخفیف",
            "تعداد",
            "بارکد"
        ])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.setAlternatingRowColors(True)                       # Alternationg
        self.setEditTriggers(QTableWidget.NoEditTriggers)        # No Edit
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row Select
        self.setSelectionMode(QAbstractItemView.SingleSelection) # Single Select
        self.verticalHeader().setVisible(False)                  # Hiden Number Row
        self.setFocusPolicy(Qt.StrongFocus)                      # Select

    def reload(self,my_products, scrool_to_buttom: bool = False):
        scroll_pos = self.verticalScrollBar().value()
        selected = self.currentRow()

        self.setRowCount(0)
        for data in my_products:
            self.__add_item(data)
        
        if scrool_to_buttom:
            self.scrollToBottom()
        else:
            self.verticalScrollBar().setValue(scroll_pos)

        if selected != -1:
            self.setCurrentCell(selected, 0)

    def __add_item(self, data):
        row = self.rowCount()
        self.insertRow(row)
        data = [
            row+1,
            data.get('pname'),
            data.get('price'),
            f"{data.get('discount')}%",
            data.get('no'),
            data.get('barcode')
        ]

        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            if col != 1:
                item.setTextAlignment(Qt.AlignCenter)
            else:
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row, col, item)

class ProductManagementPage(QWidget):
    def __init__(self, changer_page, foxapi):
        super().__init__()

        self.setWindowTitle("Product Manager")

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__changer_page = changer_page
        self.__foxapi = foxapi
        self.my_products = []

        self.__setup_ui()
        self.__signals()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'product_manager_page.qss'), 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

        self.showFullScreen()

    def __setup_ui(self):
        root = QVBoxLayout(self)

        self.__table = ProductsTableWidget()
        root.addWidget(self.__table)

        # buttons
        btns = QHBoxLayout()

        self.__btn_exit = QPushButton("خروج")
        self.__btn_delete = QPushButton("حذف کالا")
        self.__btn_add = QPushButton("اضافه کردن کالا")
        self.__btn_edit = QPushButton("ویرایش کالا")

        btns.addStretch()
        btns.addWidget(self.__btn_exit)
        btns.addWidget(self.__btn_delete)
        btns.addWidget(self.__btn_add)
        btns.addWidget(self.__btn_edit)
        btns.addStretch()

        root.addLayout(btns)

    def __signals(self):
        self.__table.itemClicked.connect(self.__check_btn_disabled)
        self.__btn_exit.clicked.connect(lambda: self.__changer_page.setCurrentIndex(0))
        self.__btn_delete.clicked.connect(self.__product_delete_signal)
        self.__btn_add.clicked.connect(self.__product_add_signal)
        self.__btn_edit.clicked.connect(self.__product_edit_signal)

    def showEvent(self, event):
        super().showEvent(event)
        self.my_products = self.__foxapi.get_products()
        self.__table.reload(self.my_products)

    def __product_delete_signal(self):
        pass

    def __product_add_signal(self):
        pass

    def __product_edit_signal(self):
        pass

    def __check_btn_disabled(self):
        row_selected    = self.__table.currentRow()

        if row_selected != -1:
            self.__btn_delete.setDisabled(False)
            self.__btn_add.setDisabled(False)
            self.__btn_edit.setDisabled(False)
        else:
            self.__btn_delete.setDisabled(True)
            self.__btn_add.setDisabled(True)
            self.__btn_edit.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = ProductManagementPage()
    w.show()

    sys.exit(app.exec_())
