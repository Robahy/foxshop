from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from btn_yes_no_widget import BtnYesNo
from string import digits
import sys, os


class PhoneNumberDialog(QDialog):
    confirmed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("dialog")
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.__setup_ui()
        self.__signals()

        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'phone_number_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.showFullScreen()

    def __setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,80)

        main_layout.addStretch()

        center = QHBoxLayout()

        self.phone_frame = QFrame()
        self.phone_frame.setObjectName("phone_frame")
        self.phone_frame.setFixedSize(650,130)   # اصلاح اندازه

        frame_layout = QHBoxLayout(self.phone_frame)
        frame_layout.setContentsMargins(30,0,30,0)

        self.prefix = QLabel("09")
        self.prefix.setObjectName("prefix")

        self.phone_edit = QLineEdit()
        self.phone_edit.setObjectName("phone_edit")
        self.phone_edit.setMaxLength(9)
        self.phone_edit.setPlaceholderText("---------")

        frame_layout.addWidget(self.prefix)
        frame_layout.addWidget(self.phone_edit)

        center.addStretch()
        center.addWidget(self.phone_frame)
        center.addStretch()

        main_layout.addLayout(center)

        main_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.__btns = BtnYesNo()
        btn_layout.addWidget(self.__btns)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)


    def __signals(self):
        self.phone_edit.textChanged.connect(lambda text: self.__changed_line_edit(self.phone_edit, text))
        self.__btns.ok_btn.clicked.connect(self.handle_confirm)
        self.__btns.cancel_btn.clicked.connect(self.reject)


    def __changed_line_edit(self, line_edit, text):
        text = text or '0'
        if text:
            if text[-1] in digits:
                echo = int(text)
            else:
                echo = int(text[:-1] or 0)
        else:
            echo = 0
        line_edit.setText(f"{abs(echo) or ''}")

    def handle_confirm(self):
        text = self.phone_edit.text()
        if len(text) == 9:
            self.phone_number = f"09{text}"
            self.accept()
        else:
            self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    phone_number_dialog = PhoneNumberDialog()
    if phone_number_dialog.exec_() == QDialog.Accepted:
        print(phone_number_dialog.phone_number)
    else:
        print("Canceled!")
