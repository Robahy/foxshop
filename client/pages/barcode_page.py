import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QListWidget, QListWidgetItem,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt


class BarcodePage(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barcode Manager")

        central = QWidget()
        self.setCentralWidget(central)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(500)

        self.add_button = QPushButton("Add Barcode")
        self.add_button.setFixedSize(150, 45)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.list_widget)
        center_layout.addStretch()

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)


        central.setLayout(main_layout)

        self.add_item("Milk 1L", "8691234567890")

        with open(".\\qss\\barcode_page.qss") as f:
                app.setStyleSheet(f.read())

    def add_item(self, name, barcode):

        widget = QWidget()

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size:18px;font-weight:bold;")

        barcode_label = QLabel(barcode)
        barcode_label.setAlignment(Qt.AlignCenter)
        barcode_label.setStyleSheet("font-size:12px;color:#555;")

        layout = QVBoxLayout(widget)
        layout.addWidget(name_label)
        layout.addWidget(barcode_label)

        widget.setStyleSheet("""
        background:white;
        border:1px solid #ccc;
        border-radius:6px;
        padding:10px;
        """)

        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = BarcodePage()
    window.showFullScreen()

    sys.exit(app.exec_())
