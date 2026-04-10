from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QListWidget, QFrame, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt
from dialogs import PasswordInputDialog
import sys, os


class SelectFoxShoperPage(QWidget):
    def __init__(self, changer_page, foxapi):
        super().__init__()

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__changer_page = changer_page
        self.__foxapi = foxapi
        self.__setup_ui()
        self.signals()
        try:
            qss_path = os.path.join(self.__BASE_DIR, '..', 'qss', 'select_foxshoper_page.qss')
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.__personnel_cash_list = []
        self.showFullScreen()

    def __setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setObjectName("main-layout")
        main_layout.setContentsMargins(60, 100, 60, 100)
        main_layout.setSpacing(40)

        title = QLabel("انتخواب فروشنده")
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        center_layout = QHBoxLayout()
        center_layout.addStretch()

        frame = QFrame()

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)

        self.__list = QListWidget()
        self.__list.setFixedSize(600, 500)

        frame_layout.addWidget(self.__list)

        center_layout.addWidget(frame)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)

    def signals(self):
        self.__list.itemDoubleClicked.connect(self.__selected_signal)

    def __selected_signal(self):
        row = self.__list.currentRow()
        if row != -1:
            # get password
            password_dlg = PasswordInputDialog()
            if password_dlg.exec_() == QDialog.Accepted:
                id = self.__personnel_cash_list[row].get('id')
                if (self.__foxapi.verify_pass_cash(
                    id       = id,
                    password = password_dlg.password
                )):
                    self.__changer_page.widget(1).set_personnel(id, 
                                                                self.__personnel_cash_list[row].get('fname'),
                                                                self.__personnel_cash_list[row].get('face_id')
                                                                ) # fun action XD
                    self.__changer_page.setCurrentIndex(1)

    def showEvent(self, event):
        super().showEvent(event)
        self.__personnel_cash_list = self.__foxapi.get_personnel_cash_all()
        self.__list.clear()
        self.__list.addItems([i.get('fname') for i in self.__personnel_cash_list])

    def keyPressEvent(self, event):
        # Enter = accept
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.__selected_signal()

        # Esc = reject
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.__changer_page.setCurrentIndex(0)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SelectFoxShoperPage([
        "Ali Ahmadi",
        "Sara Mohammadi",
        "Reza Karimi",
        "Mina Hosseini",
        "Arash Nazari"
    ])

    w.show()
    sys.exit(app.exec_())
