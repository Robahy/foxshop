import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QPushButton, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from dialogs import YesNoDialog, ProductEditorDialog

class ProductsTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__DIR_FACES = os.path.join(BASE_DIR, '..', 'static', 'faces')

        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "شماره سطر",
            "عکس پرسنلی",
            "نام",
            "کد پرسنلی",
            "سمت",
            "Bale ID"
        ])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.setAlternatingRowColors(True)                       # Alternationg
        self.setEditTriggers(QTableWidget.NoEditTriggers)        # No Edit
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row Select
        self.setSelectionMode(QAbstractItemView.SingleSelection) # Single Select
        self.verticalHeader().setVisible(False)                  # Hiden Number Row
        self.setFocusPolicy(Qt.StrongFocus)                      # Select

    def reload(self,my_personnel, scrool_to_buttom: bool = False):
        scroll_pos = self.verticalScrollBar().value()
        selected = self.currentRow()

        self.setRowCount(0)
        for data in my_personnel:
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
        level = data.get('level')
        match level:
            case 1:
                level = "normal"
            case 2:
                level = "cash"
            case 3:
                level = "supervisor"
            case 4:
                level = "manager"
        data = [
            row+1,
            data.get('face_id'),
            data.get('fname'),
            data.get('code'),
            level,
            data.get('bale_id')
        ]

        for col, value in enumerate(data):
            if col == 1:
                # PIC Personnel
                face_pic = QPixmap(os.path.join(self.__DIR_FACES, value))
                if face_pic.isNull():
                    face_pic = QPixmap(os.path.join(self.__DIR_FACES, 'base.jpg'))
                lbl = QLabel()
                lbl.setPixmap(face_pic.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                lbl.setAlignment(Qt.AlignCenter)
                self.setCellWidget(row, 1, lbl)
            else:
                item = QTableWidgetItem(str(value))
                if col != 2:
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.setItem(row, col, item)
                


class PersonnelManagerPage(QWidget):
    def __init__(self, changer_page, foxapi):
        super().__init__()

        self.setWindowTitle("Product Manager")

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__changer_page = changer_page
        self.__foxapi = foxapi
        self.my_personnel = []

        self.__setup_ui()
        self.__signals()
        self.__check_btn_disabled()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'personnel_manager_page.qss'), 'r') as f:
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
        self.__btn_delete = QPushButton("حذف پرسنل")
        self.__btn_edit = QPushButton("ویرایش اطلاعات")
        self.__btn_add = QPushButton("پرسنل جدید")

        btns.addStretch()
        btns.addWidget(self.__btn_exit)
        btns.addWidget(self.__btn_delete)
        btns.addWidget(self.__btn_edit)
        btns.addWidget(self.__btn_add)
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
        self.my_personnel = self.__foxapi.get_personnels()
        self.__table.reload(self.my_personnel)

    def __product_delete_signal(self):
        try:
            row = self.__table.currentRow()
            if row != -1:
                yes_no = YesNoDialog('آیا میخواهید کالا حذف شود؟')
                if yes_no.exec_() == QDialog.Accepted:
                    res = self.__foxapi.delete_product_by_id(self.my_products[row].get('id'))
                    if res.status_code == 204:
                        self.my_products.pop(row)
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_products)
            self.__check_btn_disabled()


    def __product_add_signal(self):
        try:
            in_p = ProductEditorDialog()
            if in_p.exec_() == QDialog.Accepted:
                product = {
                    'pname'   : in_p.pname,
                    'price'   : in_p.price,
                    'off'     : in_p.off,
                    'no'      : in_p.no,
                    'barcode' : in_p.barcode
                }
                res = self.__foxapi.create_product(product)
                if res.status_code == 201:
                    self.my_products.append(res.json())
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_products)
            self.__check_btn_disabled()

    def __product_edit_signal(self):
        try:
            row = self.__table.currentRow()
            if row != -1:
                product:dict = self.my_products[row]
                in_p = ProductEditorDialog(
                    pname   = product.get('pname'),
                    price   = product.get('price'),
                    off     = product.get('off'),
                    no      = product.get('no'),
                    barcode = product.get('barcode'),
                    is_edit = True
                )
                if in_p.exec_() == QDialog.Accepted:
                    update_product = {
                        'id'      : product.get('id'),
                        'pname'   : in_p.pname,
                        'price'   : in_p.price,
                        'off'     : in_p.off,
                        'no'      : in_p.no,
                        'barcode' : in_p.barcode
                    }
                    res = self.__foxapi.edit_product_by_id(update_product)
                    if res.status_code == 200:
                        self.my_products[row] = res.json()
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_products)
            self.__check_btn_disabled()

    def __check_btn_disabled(self):
        row_selected    = self.__table.currentRow()

        if row_selected != -1:
            self.__btn_delete.setDisabled(False)
            self.__btn_edit.setDisabled(False)
        else:
            self.__btn_delete.setDisabled(True)
            self.__btn_edit.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = PersonnelManagerPage()
    w.show()

    sys.exit(app.exec_())