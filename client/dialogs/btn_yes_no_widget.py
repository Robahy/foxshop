from PyQt5.QtWidgets import QPushButton,QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

class BtnYesNo(QFrame):
    def __init__(self, yes_msg:str='تأیید', no_msg:str='لغو'):
        super().__init__()
        self.setStyleSheet("""
            QPushButton#return{
                background: #3a3a3a;
                color:white;
                border:1px solid #555;
                border-radius:12px;
                font-size:24px;
                min-width:200px;
                padding: 20px;
            }
            QPushButton#return:hover{
                background: #4a4a4a;
                border-color: #ff8c2a;
            }
            QPushButton#return:pressed{
                background: #2a2a2a;
                border-color: #ff8c2a;
            }
        """)
        btns_layout = QHBoxLayout(self)
        btns_layout.setAlignment(Qt.AlignCenter)
        btns_layout.setSpacing(100)

        self.ok_btn = QPushButton(yes_msg)
        self.ok_btn.setObjectName('return')
        self.cancel_btn = QPushButton(no_msg)
        self.cancel_btn.setObjectName('return')

        btns_layout.addWidget(self.ok_btn)
        btns_layout.addWidget(self.cancel_btn)