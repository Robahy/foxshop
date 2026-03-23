from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt
import sys, subprocess, os


class ConfigServerDialog(QDialog):
    def __init__(self, fast_api):
        super().__init__()

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(520, 360)

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__fast_api = fast_api
        self.__setup_ui()
        self.__signals()
        try:
            qss_path = os.path.join(self.__BASE_DIR, '..', 'qss', 'config_server.qss')
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

    def __setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30,25,30,25)

        title = QLabel("تنظیم اتصال به سرور")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        form = QGridLayout()
        form.setVerticalSpacing(14)
        form.setHorizontalSpacing(12)

        host_lbl = QLabel("Host")
        self.__host = QLineEdit()

        port_lbl = QLabel("Port")
        self.__port = QLineEdit()

        user_lbl = QLabel("Username")
        self.__user = QLineEdit()

        pass_lbl = QLabel("Password")
        self.__password = QLineEdit()
        self.__password.setEchoMode(QLineEdit.Password)

        form.addWidget(host_lbl,0,0)
        form.addWidget(self.__host,0,1)

        form.addWidget(port_lbl,1,0)
        form.addWidget(self.__port,1,1)

        form.addWidget(user_lbl,2,0)
        form.addWidget(self.__user,2,1)

        form.addWidget(pass_lbl,3,0)
        form.addWidget(self.__password,3,1)

        btn_layout = QHBoxLayout()

        self.__cancel_btn = QPushButton("لغو اتصال")
        self.__connect_btn = QPushButton("اتصال")


        btn_layout.addStretch()
        btn_layout.addWidget(self.__cancel_btn)
        btn_layout.addWidget(self.__connect_btn)

        main_layout.addWidget(title)
        main_layout.addLayout(form)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def __signals(self):
        self.__cancel_btn.clicked.connect(self.__disconnect)
        self.__connect_btn.clicked.connect(self.__connect)

    def __connect(self):
        if not (self.__host.text() and self.__port.text() and self.__user.text() and self.__password.text()):
            self.__fast_api.start()
            self.accept()

    def __disconnect(self):
        self.__fast_api.stop()
        self.reject()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config_server_dialg = ConfigServerDialog()
    config_server_dialg.exec_()
