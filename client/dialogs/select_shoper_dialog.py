import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QListWidget, 
                            QLabel, QFrame, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import winsound

class SelectShoperDialog(QDialog):
    def __init__(self, fastapi):
        super().__init__()
        
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.fastapi = fastapi

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(600, 600)
        
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'select_shoper_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except:
            pass
            
        
        main_layout = QVBoxLayout(self)
        main_layout.setObjectName("main-layout")
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title_label = QLabel("Select Fox Shoper")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_frame.setFrameShadow(QFrame.Sunken)
        
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)

        self.__vendor_list = QListWidget()
        self.__vendor_list.setFont(QFont("Tahoma", 13))
        
        self.shopers = self.fastapi.get_shoper()
        self.__vendor_list.addItems(self.shopers)
        
        list_layout.addWidget(self.__vendor_list)
        
        self.__password_edit = QLineEdit()
        self.__password_edit.setPlaceholderText("Enter password")
        self.__password_edit.setEchoMode(QLineEdit.Password)
        self.__password_edit.setFont(QFont("Tahoma", 12))

        main_layout.addWidget(self.__password_edit)
        main_layout.addWidget(list_frame)
        
        self.__vendor_list.itemDoubleClicked.connect(self.check_password)
        self.__password_edit.returnPressed.connect(self.check_password)
        
        self.setModal(True)

    def check_password(self):
        row      = self.__vendor_list.currentRow()
        password = self.__password_edit.text()
        if row != -1 and password and self.fastapi.verify_cashier(row, password):
            self.accept_selection()
        else:
            winsound.MessageBeep()

    def accept_selection(self):
        row         = self.__vendor_list.currentRow()
        self.id     = row
        self.name   = self.shopers[row]
        self.accept()

    def closeEvent(self, event):
        event.ignore()
        winsound.MessageBeep()

    def reject(self):
        winsound.MessageBeep()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    shoper = SelectShoperDialog()
    shoper.exec_()
    print(f"Selected ID   : {shoper.id}")
    print(f"Selected NAME : {shoper.name}")
    sys.exit(0)
