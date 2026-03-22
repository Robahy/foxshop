from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys, os


class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__setup_ui()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'main_page.qss'), 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

        self.showFullScreen()

    def __setup_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)

        image = QLabel()
        image.setObjectName("image")
        image.setAlignment(Qt.AlignCenter)

        pix = QPixmap(os.path.join(self.__BASE_DIR, '..', 'static', 'icon.png'))
        image.setPixmap(
            pix.scaled(
                300, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        image_layout.addStretch()
        image_layout.addWidget(image)
        image_layout.addStretch()

        # -------- پنل دکمه‌ها --------
        panel = QWidget()
        panel.setObjectName("panel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(15, 15, 15, 15)

        start_shop = QPushButton("شروع برنامه")
        start_shop.setDisabled(True)
        config_server = QPushButton("راه اندازی سرور")
        product_manager = QPushButton("مدریت کالا ها")
        pay_manager = QPushButton("مدریت فروش")

        panel_layout.addWidget(start_shop)
        panel_layout.addWidget(config_server)
        panel_layout.addWidget(product_manager)
        panel_layout.addWidget(pay_manager)
        panel_layout.addStretch()

        root.addWidget(image_container, 9)
        root.addWidget(panel, 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Page()
    w.show()

    sys.exit(app.exec_())
