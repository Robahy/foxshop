from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QGridLayout, QLabel
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from .btn_yes_no_widget import BtnYesNo
from string import digits
import sys, os, winsound


class NumberDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enter number')

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__num = 0

        self.__setup_ui()
        self.__signals()
        try:
            qss_path = os.path.join(self.__BASE_DIR, '..', 'qss', 'number_dialog.qss')
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass
        self.showFullScreen()
        self.line_edit.setFocus()

    def __setup_ui(self):
        BUTTON_W, BUTTON_H = 100, 80
        GRID_SPACING = 12

        main_layout = QVBoxLayout()

        title = QLabel("تعداد")
        title.setObjectName("cashTitle")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        main_layout.addSpacing(30)

        middle_h = QHBoxLayout()
        middle_h.addStretch()

        center = QHBoxLayout()
        left = QVBoxLayout()

        keypad_width = 3 * BUTTON_W + 2 * GRID_SPACING
        self.line_edit = QLineEdit(f"{self.__num}")
        self.line_edit.setFocusPolicy(Qt.StrongFocus)
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
        self.line_edit.textChanged.connect(self.__changed_line_edit)
        self.__btns.ok_btn.clicked.connect(self.accept)
        self.__btns.cancel_btn.clicked.connect(self.reject)

    def __num_pad_clicked(self, text):
        content = self.line_edit.text()
        if text == "C":
            content = '0'
        elif text == "⌫":
            content = content[:-1] or '0'
        else:
            if content == '0':
                content = text
            else:
                content += text
        self.__num = int(content)
        self.line_edit.setText(f"{content}")
        self.line_edit.setFocus()

    def __changed_line_edit(self, text):
        filtered = int("".join(ch for ch in text if ch in digits) or "0")
        self.__num = int(filtered)
        self.line_edit.setText(f"{filtered,}")
        self.line_edit.setFocus()

    def closeEvent(self, event):
        event.ignore()
        winsound.MessageBeep()
    
    @property
    def number(self):
        return self.__num

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cash = NumberDialog()
    if cash.exec_() == QDialog.Accepted:
        print(f"{cash.number}")
    else:
        print("Canceled!")