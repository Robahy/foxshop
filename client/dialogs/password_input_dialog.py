from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QGridLayout, QLabel
)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt
from .btn_yes_no_widget import BtnYesNo
from string import digits
import sys, os, winsound


class PasswordInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Password")

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__pwd = ""

        self.__setup_ui()
        self.__signals()

        try:
            qss_path = os.path.join(self.__BASE_DIR, "..", "qss", "number_dialog.qss")
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.showFullScreen()
        self.line_edit.setFocus()

    def __setup_ui(self):
        BUTTON_W, BUTTON_H = 120, 100
        GRID_SPACING = 15

        main_layout = QVBoxLayout()
        main_layout.setSpacing(35)

        title = QLabel("رمز عبور")
        title.setObjectName("cashTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Tahoma", 34))
        main_layout.addWidget(title)

        main_layout.addSpacing(20)

        # وسط چین
        middle = QHBoxLayout()
        middle.addStretch()

        center = QVBoxLayout()

        # لاین ادیت پسورد
        self.line_edit = QLineEdit()
        self.line_edit.setFixedHeight(70)
        self.line_edit.setFixedWidth(400)
        self.line_edit.setFont(QFont("Tahoma", 26))
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setValidator(QIntValidator())
        center.addWidget(self.line_edit, alignment=Qt.AlignCenter)

        center.addSpacing(25)

        # کیپد عددی
        grid = QGridLayout()
        grid.setSpacing(GRID_SPACING)

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("⌫", 3, 0), ("0", 3, 1), ("C", 3, 2),
        ]

        for text, r, c in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(BUTTON_W, BUTTON_H)
            btn.setFont(QFont("Tahoma", 22))
            btn.clicked.connect(lambda _, t=text: self.__num_pad_clicked(t))
            grid.addWidget(btn, r, c)

        center.addLayout(grid)

        middle.addLayout(center)
        middle.addStretch()

        self.__btns = BtnYesNo()

        main_layout.addStretch()
        main_layout.addLayout(middle)
        main_layout.addWidget(self.__btns)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def __signals(self):
        self.line_edit.textChanged.connect(self.__changed_line_edit)
        self.__btns.ok_btn.clicked.connect(self.accept)
        self.__btns.cancel_btn.clicked.connect(self.reject)

    def __num_pad_clicked(self, text):
        content = self.line_edit.text()

        if text == "C":
            self.line_edit.setText("")
        elif text == "⌫":
            self.line_edit.setText(content[:-1])
        else:
            self.line_edit.setText(content + text)

        self.line_edit.setFocus()

    def __changed_line_edit(self, text):
        filtered = "".join(ch for ch in text if ch in digits)
        self.__pwd = filtered
        self.line_edit.setText(f"{filtered}")
        self.line_edit.setFocus()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        event.ignore()
        winsound.MessageBeep()

    @property
    def password(self):
        return self.__pwd


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = PasswordInputDialog()
    if d.exec_() == QDialog.Accepted:
        print("Password:", d.password)
    else:
        print("Canceled")