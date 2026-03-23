from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from dialogs.config_server_dialog import ConfigServerDialog
import sys, os


class MainPage(QWidget):
    def __init__(self, changer_page, fastapi):
        super().__init__()
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__changer_page = changer_page
        self.__fastapi = fastapi
        self.__setup_ui()
        self.__signals()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'main_page.qss'), 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

        self.showFullScreen()
        # blink signal light server
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__blink_btn_server)
        self.__set_blink_btn_light_server(False)

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

        self.__btn_start_shop = QPushButton("شروع برنامه")
        self.__btn_start_shop.setDisabled(True)
        self.__btn_config_server = QPushButton("راه اندازی سرور")
        self.__circle_green = QLabel(self.__btn_config_server)
        self.__circle_green.setGeometry(10, 25, 12, 12)
        self.__circle_green.setObjectName("circle-green")
        self.__btn_product_manager = QPushButton("مدریت کالا ها")
        self.__btn_pay_manager = QPushButton("مدریت فروش")
        self.__btn_exit = QPushButton("خروج")

        panel_layout.addWidget(self.__btn_start_shop)
        panel_layout.addWidget(self.__btn_config_server)
        panel_layout.addWidget(self.__btn_product_manager)
        panel_layout.addWidget(self.__btn_pay_manager)
        panel_layout.addWidget(self.__btn_exit)
        panel_layout.addStretch()

        root.addWidget(image_container, 9)
        root.addWidget(panel, 2)

    def __signals(self):
        self.__btn_config_server.clicked.connect(self.__btn_config_server_sinal)
        self.__btn_exit.clicked.connect(lambda: self.window().close())

    def __btn_config_server_sinal(self):
        config_server_dialg = ConfigServerDialog(self.__fastapi)
        if config_server_dialg.exec_() == QDialog.Accepted:
            self.__btn_start_shop.setDisabled(False)
            self.__set_blink_btn_light_server(True)
        else:
            self.__btn_start_shop.setDisabled(True)
            self.__set_blink_btn_light_server(False)

    def __set_blink_btn_light_server(self,  is_light: bool | None=True):
        if is_light:
            self.__visible = False
            self.__timer.start(700)
        else:
            self.__timer.stop()
            self.__circle_green.setStyleSheet("background-color: transparent; border-radius:6px;")
            
    def __blink_btn_server(self):
        if self.__visible:
            self.__circle_green.setStyleSheet("background-color: transparent; border-radius:6px;")
        else:
            self.__circle_green.setStyleSheet("background-color: green; border-radius:6px;")
        self.__visible = not self.__visible

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainPage()
    w.show()

    sys.exit(app.exec_())
