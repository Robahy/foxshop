from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QGridLayout, QLabel
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from string import digits
import sys, os


class CashPage(QWidget):
    def __init__(self, max:int):
        super().__init__()
        self.setWindowTitle('cash page')

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.max = max
        self.cash_num = self.max


        self.__setup_ui()
        self.__load_qss()
        self.showFullScreen()

        self.line_edit.setFocus()

    def __load_qss(self):
        try:
            qss_path = os.path.join(self.__BASE_DIR, '..', 'qss', 'cash_page.qss')
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("QSS load failed:", e)

    def __setup_ui(self):
        BUTTON_W, BUTTON_H = 100, 80
        SIDE_BTN_W, SIDE_BTN_H = 160, 80
        BOTTOM_BTN_W, BOTTOM_BTN_H = 200, 80
        GRID_SPACING = 12

        outer = QVBoxLayout()

        # ===== عنوان بالا =====
        title = QLabel("پرداخت نقدی")
        title.setObjectName("cashTitle")
        title.setAlignment(Qt.AlignCenter)
        outer.addWidget(title)

        outer.addSpacing(30)

        # ===== بخش اصلی =====
        middle_h = QHBoxLayout()
        middle_h.addStretch()

        center = QHBoxLayout()
        left = QVBoxLayout()

        keypad_width = 3 * BUTTON_W + 2 * GRID_SPACING
        self.line_edit = QLineEdit(f"{self.max:,}")
        self.line_edit.setFocusPolicy(Qt.StrongFocus)
        self.line_edit.textChanged.connect(self.__changed_line_edit)
        self.line_edit.setFixedWidth(keypad_width)
        self.line_edit.setFixedHeight(50)
        left.addWidget(self.line_edit)

        grid = QGridLayout()
        grid.setSpacing(GRID_SPACING)

        buttons = [
            ('7',0,0), ('8',0,1), ('9',0,2),
            ('4',1,0), ('5',1,1), ('6',1,2),
            ('1',2,0), ('2',2,1), ('3',2,2),
            ('⌫',3,0), ('0',3,1), ('C',3,2)
        ]

        for text,r,c in buttons:
            b = QPushButton(text)
            b.setFixedSize(BUTTON_W, BUTTON_H)
            b.clicked.connect(lambda _,t=text:self.num_pad_clicked(t))
            grid.addWidget(b, r, c)

        left.addLayout(grid)

        right = QVBoxLayout()

        btn_fix = QPushButton(f"{self.max:,}")
        btn_fix.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        btn_fix.clicked.connect(self.close)
        right.addWidget(btn_fix)

        btn_50 = QPushButton(f"50,000")
        btn_50.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        btn_50.clicked.connect(self.__add_50)
        right.addWidget(btn_50)

        btn_10 = QPushButton(f"10,000")
        btn_10.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        btn_10.clicked.connect(self.__add_10)
        right.addWidget(btn_10)

        center.addLayout(left)
        center.addSpacing(30)
        center.addLayout(right)

        middle_h.addLayout(center)
        middle_h.addStretch()

        outer.addStretch()
        outer.addLayout(middle_h)
        outer.addStretch()

        # ===== دکمه‌های پایین =====
        bottom = QHBoxLayout()
        bottom.addStretch()

        confirm_btn = QPushButton("تأیید")
        cancel_btn = QPushButton("لغو")

        confirm_btn.clicked.connect(self.close)
        cancel_btn.clicked.connect(self.close)

        confirm_btn.setFixedSize(BOTTOM_BTN_W, BOTTOM_BTN_H)
        cancel_btn.setFixedSize(BOTTOM_BTN_W, BOTTOM_BTN_H)

        bottom.addWidget(confirm_btn)
        bottom.addSpacing(30)
        bottom.addWidget(cancel_btn)
        bottom.addStretch()

        outer.addLayout(bottom)

        self.setLayout(outer)

    def __add_50(self):
        self.cash_num = 50000
        self.line_edit.setText(f"{self.cash_num:,}")
        self.close()
    
    def __add_10(self):
        self.cash_num = 10000
        self.line_edit.setText(f"{self.cash_num:,}")
        self.close()

    def num_pad_clicked(self, text):
        content = self.line_edit.text()
        if text == "C":
            self.line_edit.setText('0')
        elif text == "⌫":
            if len(content) <= 1:
                self.cash_num = 0
            else:
                self.line_edit.setText(self.line_edit.text()[:-1])
        else:
            if content == '0':
                self.line_edit.setText(text)
            else:
                self.line_edit.setText(self.line_edit.text() + text)
        self.line_edit.setText(f"{self.cash_num:,}")
        self.line_edit.setFocus()

    def __changed_line_edit(self, text):
        if (text and text[-1] in digits):
            self.cash_num = int(text.replace(',', '') or 0)
        else:
            self.cash_num = 0
        self.line_edit.setText(f"{self.cash_num:,}")
        self.line_edit.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CashPage(200000)
    window.show()
    sys.exit(app.exec_())
