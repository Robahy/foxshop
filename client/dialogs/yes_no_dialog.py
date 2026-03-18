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
        self.__setup_ui(message)
        self.__signals()
        
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'yes_no_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.showFullScreen()

    def __setup_ui(self, msg):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        lbl_warning = QLabel()
        lbl_warning.setObjectName("lbl_warning")
        warning_icon = QPixmap(os.path.join(self.__BASE_DIR, '..', 'static', 'warning.png'))
        lbl_warning.setPixmap(warning_icon.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lbl_warning.setAlignment(Qt.AlignCenter)

        msg = QLabel(msg)
        msg.setObjectName("msg")
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)

        btns = QHBoxLayout()
        btns.setAlignment(Qt.AlignCenter)
        btns.setSpacing(100)

        self.__ok_btn = QPushButton("تأیید")
        self.__ok_btn.setObjectName('return')
        self.__cancel_btn = QPushButton("لغو")
        self.__cancel_btn.setObjectName('return')

        # Add btns
        btns.addWidget(self.__ok_btn)
        btns.addWidget(self.__cancel_btn)
        # Add 
        main_layout.addWidget(msg)
        main_layout.addWidget(lbl_warning)
        main_layout.addLayout(btns)
        self.setLayout(main_layout)

    def __signals(self):
        self.__ok_btn.clicked.connect(self.accept)
        self.__cancel_btn.clicked.connect(self.reject)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    yes_no_dialog = YesNoDialog("Are you ok?")
    print(yes_no_dialog.exec_() == QDialog.Accepted)