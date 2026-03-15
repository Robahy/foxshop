from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStyle
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys, os


class YesNoDialog(QDialog):
    def __init__(self, message: str):
        super().__init__()

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'yes_no_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        lbl_warning = QLabel()
        lbl_warning.setObjectName("lbl_warning")
        warning_icon = QPixmap(os.path.join(self.__BASE_DIR, '..', 'static', 'warning.png'))
        lbl_warning.setPixmap(warning_icon.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lbl_warning.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_warning)

        msg = QLabel(message)
        msg.setObjectName("msg")
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)
        layout.addWidget(msg)

        btns = QHBoxLayout()
        btns.setAlignment(Qt.AlignCenter)
        btns.setSpacing(100)

        ok_btn = QPushButton("تأیید")
        cancel_btn = QPushButton("لغو")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)

        layout.addLayout(btns)

        self.setLayout(layout)
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    yes_no_dialog = YesNoDialog("Are you ok?")
    print(yes_no_dialog.exec_() == QDialog.Accepted)