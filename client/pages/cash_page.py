from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QGridLayout
)
import sys


class KeypadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("صفحه پرداخت")
        self.setup_ui()
        self.apply_style()
        self.showFullScreen()

    def setup_ui(self):
        BUTTON_W, BUTTON_H = 100, 80
        SIDE_BTN_W, SIDE_BTN_H = 160, 80
        BOTTOM_BTN_W, BOTTOM_BTN_H = 200, 80
        GRID_SPACING = 12

        outer = QVBoxLayout()
        outer.addStretch()

        middle_h = QHBoxLayout()
        middle_h.addStretch()

        center = QHBoxLayout()

        # سمت چپ
        left = QVBoxLayout()
        keypad_width = 3 * BUTTON_W + 2 * GRID_SPACING

        self.line_edit = QLineEdit()
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
            b.clicked.connect(lambda _,t=text:self.button_clicked(t))
            grid.addWidget(b, r, c)

        left.addLayout(grid)

        # سمت راست
        right = QVBoxLayout()
        for label in ["کل مبلغ", "50,000", "10,000"]:
            b = QPushButton(label)
            b.setFixedSize(SIDE_BTN_W, SIDE_BTN_H)
            right.addWidget(b)

        center.addLayout(left)
        center.addSpacing(30)
        center.addLayout(right)

        middle_h.addLayout(center)
        middle_h.addStretch()

        outer.addLayout(middle_h)
        outer.addStretch()

        # پایین صفحه
        bottom = QHBoxLayout()
        bottom.addStretch()

        cancel_btn = QPushButton("لغو")
        confirm_btn = QPushButton("تأیید")
        cancel_btn.setObjectName("cancelButton")
        confirm_btn.setObjectName("confirmButton")

        cancel_btn.setFixedSize(BOTTOM_BTN_W, BOTTOM_BTN_H)
        confirm_btn.setFixedSize(BOTTOM_BTN_W, BOTTOM_BTN_H)

        bottom.addWidget(cancel_btn)
        bottom.addSpacing(30)
        bottom.addWidget(confirm_btn)
        bottom.addStretch()

        outer.addLayout(bottom)
        self.setLayout(outer)

    def button_clicked(self, text):
        if text == "C":
            self.line_edit.clear()
        elif text == "⌫":
            self.line_edit.setText(self.line_edit.text()[:-1])
        else:
            self.line_edit.setText(self.line_edit.text() + text)

    def apply_style(self):
        self.setStyleSheet("""
        QWidget{
            background:#1e1e1e;
            font-family:Tahoma;
        }
        QLineEdit{
            background:#2b2b2b;
            color:white;
            border:2px solid #3c3c3c;
            border-radius:10px;
            padding:8px;
            font-size:24px;
        }
        QPushButton{
            background:#3a3a3a;
            color:white;
            border:1px solid #555;
            border-radius:12px;
            font-size:24px;
        }
        QPushButton#cancelButton{
            background:#b22222;
        }
        QPushButton#confirmButton{
            background:#228b22;
        }
        """)
        

app = QApplication(sys.argv)
window = KeypadWindow()
window.show()
sys.exit(app.exec_())
