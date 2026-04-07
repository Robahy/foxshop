from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QGridLayout, QLabel
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from .btn_yes_no_widget import BtnYesNo
from string import digits
import sys, os, winsound


class CashDialog(QDialog):
    def __init__(self, max:int):
        super().__init__()
        self.setWindowTitle('cash page')

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.max = max
        self.__cash_num = self.max

        self.__setup_ui()
        self.__signals()
        try:
            qss_path = os.path.join(self.__BASE_DIR, '..', 'qss', 'cash_dialog.qss')
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.showFullScreen()
        self.line_edit.setFocus()

    def __setup_ui(self):
        BUTTON_W, BUTTON_H = 100, 80
        SIDE_BTN_W, SIDE_BTN_H = 160, 80
        GRID_SPACING = 12

        main_layout = QVBoxLayout()

        title = QLabel("پرداخت نقدی")
        title.setObjectName("cashTitle")
        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addSpacing(30)

        middle_h = QHBoxLayout()
        middle_h.addStretch()

        center = QHBoxLayout()
        left = QVBoxLayout()

        keypad_width = 3 * BUTTON_W + 2 * GRID_SPACING
        self.line_edit = QLineEdit("0")
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
            b.clicked.connect(lambda _,t=text:self.__num_pad_clicked(t))
            grid.addWidget(b, r, c)

        left.addLayout(grid)

        right = QVBoxLayout()

        self.__btn_fix = QPushButton(f"{self.max:,}")
        self.__btn_fix.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        right.addWidget(self.__btn_fix)

        self.__btn_50 = QPushButton("50,000")
        self.__btn_50.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        right.addWidget(self.__btn_50)

        self.__btn_10 = QPushButton("10,000")
        self.__btn_10.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
        right.addWidget(self.__btn_10)

        center.addLayout(left)
        center.addSpacing(30)
        center.addLayout(right)

        middle_h.addLayout(center)
        middle_h.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(middle_h)
        main_layout.addStretch()

        self.__btns = BtnYesNo()

        main_layout.addWidget(self.__btns)

        self.setLayout(main_layout)

    def __signals(self):
        self.__btn_fix.clicked.connect(self.accept)
        self.__btn_50.clicked.connect(self.__add_50)
        self.__btn_10.clicked.connect(self.__add_10)
        self.__btns.ok_btn.clicked.connect(self.__down)
        self.__btns.cancel_btn.clicked.connect(self.reject)


    def __add_50(self):
        self.__cash_num = 50000
        self.line_edit.setText(f"{self.cash_num:,}")
        self.accept()
    
    def __add_10(self):
        self.__cash_num = 10000
        self.line_edit.setText(f"{self.cash_num:,}")
        self.accept()

    def __down(self):
        if self.cash_num == self.max:
            self.reject()
        else:
            self.accept()

    def __num_pad_clicked(self, text):
        content = self.line_edit.text()
        if text == "C":
            self.line_edit.setText('0')
        elif text == "⌫":
            if len(content) <= 1:
                self.__cash_num = 0
            else:
                self.line_edit.setText(self.line_edit.text()[:-1])
        else:
            if content == '0':
                self.line_edit.setText(text)
            else:
                self.line_edit.setText(self.line_edit.text() + text)
        self.line_edit.setText(f"{self.__cash_num:,}")
        self.line_edit.setFocus()

    def __changed_line_edit(self, text):
        filtered = "".join(ch for ch in text.replace(',', '') or 0 if ch in digits)
        self.__cash_num = filtered
        self.line_edit.setText(f"{filtered:,}")
        self.line_edit.setFocus()

    def closeEvent(self, event):
        event.ignore()
        winsound.MessageBeep()
    
    @property
    def cash_num(self) -> int:
        return self.__cash_num

if __name__ == "__main__":
    cash = CashDialog(200000)
    status = cash.exec_() == QDialog.Accepted
    print(status)
    if status:
        print(f"{cash.cash_num:,}")