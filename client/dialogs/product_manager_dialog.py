from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt
import os, sys


class ProductManagerDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.setStyleSheet(self.qss())

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ---------- نوار بالا ----------
        header = QLabel("چک کردن قیمت")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        root_layout.addWidget(header)

        # ---------- محتوای اصلی ----------
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)

        # سمت چپ (اطلاعات)
        info = QLabel("اطلاعات کالا اینجا نمایش داده می‌شود")
        info.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # سمت راست (کی‌پد)
        keypad = QWidget()
        keypad_layout = QGridLayout(keypad)

        texts = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", ".", "←"
        ]

        for i, t in enumerate(texts):
            btn = QPushButton(t)
            keypad_layout.addWidget(btn, i // 3, i % 3)

        content_layout.addWidget(info, 6)
        content_layout.addWidget(keypad, 4)

        root_layout.addWidget(content, 1)

        # ---------- دکمه‌های پایین ----------
        footer = QWidget()
        footer.setObjectName("footer")
        footer_layout = QHBoxLayout(footer)

        btn_cancel = QPushButton("لغو")
        btn_add = QPushButton("اضافه کردن کالا")
        btn_search = QPushButton("جستجو")

        btn_cancel.clicked.connect(self.reject)

        footer_layout.addWidget(btn_cancel)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_add)
        footer_layout.addWidget(btn_search)

        root_layout.addWidget(footer)

    def qss(self):
        return """
        QDialog {
            background: #121212;
            color: white;
            font-size: 18px;
        }

        QLabel {
            color: white;
        }

        #header {
            background: #ff8c2a;
            color: black;
            padding: 16px;
            font-size: 22px;
            font-weight: bold;
        }

        QPushButton {
            background: #2a2a2a;
            border: 1px solid #444;
            padding: 14px;
            min-width: 120px;
        }

        QPushButton:hover {
            background: #3a3a3a;
        }

        QPushButton:pressed {
            background: #1e1e1e;
        }

        #footer {
            background: #181818;
            border-top: 3px solid #ff8c2a;
            padding: 12px;
        }
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    product_manager_dialog = ProductManagerDialog()
    print(product_manager_dialog.exec_() == QDialog.Accepted)