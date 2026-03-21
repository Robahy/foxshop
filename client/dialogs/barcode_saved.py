from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from .btn_yes_no_widget import BtnYesNo
import sys, csv, os


class BarcodesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barcodes saved")
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.__setup_ui()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'barcode_saved_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass
        self.__signals()

    def __setup_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel("بارکد های ذخیره شده")
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)

        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(15)
        grid_layout.setAlignment(Qt.AlignCenter)

        try:
            if not os.path.exists("barcode_saved.csv"):
                with open(os.path.join(self.__BASE_DIR, '..', 'barcode_saved.csv'), "w", newline="", encoding="utf-8") as f:
                    csv.DictWriter(f, fieldnames=["name", "barcode"]).writeheader()
            row, col = 0, 0
            with open(os.path.join(self.__BASE_DIR, '..', 'barcode_saved.csv'), newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for item in reader:
                    name = item["name"]
                    barcode = item["barcode"]

                    btn = QPushButton()
                    btn.clicked.connect(self.__barcode_btn_presed_signal())
                    btn.setText(f"{name}\n{barcode}")

                    grid_layout.addWidget(btn, row, col)

                    col += 1
                    if col == 4:
                        col = 0
                        row += 1
        except Exception:
            pass
        finally:
                self.__add_btn = QPushButton("➕\nافزودن بارکد")
                grid_layout.addWidget(self.__add_btn, row+1, 1)

        self.__btns = BtnYesNo(self)

        # Add main_layout
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(grid_container)
        main_layout.addStretch()
        main_layout.addLayout(self.__btns)

    def __signals(self):
            self.__btns.cancel_btn.clicked.connect(self.reject)
            self.__btns.ok_btn.clicked.connect(self.accept)
            self.__add_btn.clicked.connect(self.__add_barcode_saved_signal)

    def __barcode_btn_presed_signal(self):
        pass

    def __add_barcode_saved_signal(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    barcode_saved_dialog = BarcodesDialog()
    barcode_saved_dialog.showFullScreen()

    sys.exit(barcode_saved_dialog.exec_())