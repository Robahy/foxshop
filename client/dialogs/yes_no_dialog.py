from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStyle
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .btn_yes_no_widget import BtnYesNo
import os


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

        lbl_msg = QLabel(msg)
        lbl_msg.setObjectName("msg")
        lbl_msg.setAlignment(Qt.AlignCenter)

        self.__btns = BtnYesNo(yes_msg='بله', no_msg='خیر')
        
        # Add Total
        main_layout.addWidget(lbl_warning)
        main_layout.addWidget(lbl_msg)
        main_layout.addWidget(self.__btns)
        self.setLayout(main_layout)

    def __signals(self):
        self.__btns.ok_btn.clicked.connect(self.accept)
        self.__btns.cancel_btn.clicked.connect(self.reject)


    
if __name__ == "__main__":
    yes_no_dialog = YesNoDialog("Are you ok?")
    print(yes_no_dialog.exec_() == QDialog.Accepted)