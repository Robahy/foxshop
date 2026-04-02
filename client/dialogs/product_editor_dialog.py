from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from string import digits
import sys, os


class ProductEditorDialog(QDialog):
    def __init__(self,
                pname   : str = '',
                price   : int = 0,
                off     : int = 0,
                no      : int = 0,
                barcode : str = '',
                is_edit : bool = False ):
        super().__init__()

        self.setWindowTitle("Editor Product")
        self.setFixedSize(450, 360)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.pname   = pname
        self.price   = price
        self.off     = off
        self.no      = no
        self.barcode = barcode
        self.is_edit = is_edit
        self.__setup_ui()
        self.__signals()
        self.__check_accept_disabled()

        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'product_editro_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

    def __setup_ui(self):

        title = QLabel("ویرایشگر کالا")
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()

        self.name_edit = QLineEdit(self.pname)
        self.price_edit = QLineEdit(f"{self.price:,}")
        self.off_edit = QLineEdit(f"{self.off}")
        self.no_edit = QLineEdit(f"{self.no:,}")
        self.barcode_edit = QLineEdit(f"{self.barcode}")
        self.barcode_edit.setReadOnly(self.is_edit)

        grid.addWidget(QLabel("اسم کالا"), 0, 0)
        grid.addWidget(self.name_edit, 0, 1)

        grid.addWidget(QLabel("قیمت کالا"), 1, 0)
        grid.addWidget(self.price_edit, 1, 1)

        grid.addWidget(QLabel("تخفیف (%)"), 2, 0)
        grid.addWidget(self.off_edit, 2, 1)

        grid.addWidget(QLabel("موجودی"), 3, 0)
        grid.addWidget(self.no_edit, 3, 1)

        grid.addWidget(QLabel("بارکد کالا"), 4, 0)
        grid.addWidget(self.barcode_edit, 4, 1)

        self.cancel_btn      = QPushButton("لغو")
        self.save_change_btn = QPushButton("ذخیره تغییرات")


        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_change_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

    def __signals(self):
        self.price_edit.textChanged.connect(lambda text: self.__changed_line_edit(self.price_edit, text))
        self.off_edit.textChanged.connect(self.__changed_off_edit)
        self.no_edit.textChanged.connect(lambda text: self.__changed_line_edit(self.no_edit, text))
        self.barcode_edit.textChanged.connect(self.__changed_barcode_edit)
        self.accepted.connect(self.__on_accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_change_btn.clicked.connect(self.accept)
    
    def __changed_line_edit(self, line_edit, text):
        text = text.replace(',', '') or '0'
        if text:
            if text[-1] in digits:
                echo = int(text)
            else:
                echo = int(text[:-1] or 0)
        else:
            echo = 0
        line_edit.setText(f"{abs(echo):,}")
        line_edit.setFocus()
        self.__check_accept_disabled()

    def __changed_off_edit(self, text):
        text = text or '0'
        if text:
            if text[-1] in digits:
                if int(text) <= 100:
                    echo = int(text)
                else:
                    echo = int(text[:-1] or 0)
            else:
                echo = int(text[:-1] or 0)
        else:
            echo = 0
        self.off_edit.setText(f"{abs(echo)}")
        self.off_edit.setFocus()
        self.__check_accept_disabled()

    def __changed_barcode_edit(self, text):
        text = text or '0'
        if text:
            if text[-1] in digits:
                echo = int(text)
            else:
                echo = int(text[:-1] or 0)
        else:
            echo = ''
        self.barcode_edit.setText(f"{abs(echo) or ''}")
        self.barcode_edit.setFocus()    
        self.__check_accept_disabled()

    def __on_accept(self):
        self.pname   = self.name_edit.text().replace(',', '') or '0'
        self.price   = int(self.price_edit.text().replace(',', '') or '0')
        self.off     = int(self.off_edit.text())
        self.no      = int(self.no_edit.text().replace(',', '') or '0')
        self.barcode = self.barcode_edit.text().replace(',', '') or '0'

    def __check_accept_disabled(self):
        self.save_change_btn.setDisabled(not (
            self.name_edit.text() and
            self.price_edit.text() != '0' and
            self.barcode_edit.text()
        ))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dlg = ProductEditorDialog(pname="test")
    if dlg.exec_() == QDialog.Accepted:
        print(f"pname   : {dlg.pname}")
        print(f"price   : {dlg.price}")
        print(f"off     : {dlg.off}%")
        print(f"no      : {dlg.no}")
        print(f"barcode : {dlg.barcode}")
    else:
        print("canceled")

    sys.exit(0)