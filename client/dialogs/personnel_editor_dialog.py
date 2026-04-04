from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout,
    QFileDialog, QWidget, QApplication, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from string import digits
import sys, os


class LevelSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.normal_btn = QPushButton("معمولی")
        self.normal_btn.setObjectName("start")

        self.cashier_btn = QPushButton("صندوقدار")
        self.cashier_btn.setObjectName('center')

        self.supervisor_btn = QPushButton("سرپرست")
        self.supervisor_btn.setObjectName("end")

        buttons = [
            (self.normal_btn, 1),
            (self.cashier_btn, 2),
            (self.supervisor_btn, 3)
        ]

        for btn, level in buttons:
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda _, l=level: self.set_level(l))

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(self.normal_btn)
        layout.addWidget(self.cashier_btn)
        layout.addWidget(self.supervisor_btn)

        self.set_level(1)

    def set_level(self, level):
        self.__level = level
        match level:
            case 1:
                self.normal_btn.setChecked(True)
            case 2:
                self.cashier_btn.setChecked(True)
            case 3:
                self.supervisor_btn.setChecked(True)

    @property
    def level(self):
        return int(self.__level)


class PersonnelEditorDialog(QDialog):
    def __init__(self,
                fname   : str  = '',
                face_id : str  = 'base.jpg',
                level   : int  = 1,
                bale_id : str  = '',
                code    : str  = '',
                is_edit : bool = False
        ):
        super().__init__()
        self.setWindowTitle("Editor personnel")
        self.setFixedSize(600, 450)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'personnel_editor_dialog.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass

        self.fname         = fname
        self.face_id       = face_id
        self.password_hash = ""
        self.password_cash = ""
        self.level         = level
        self.bale_id       = bale_id
        self.code          = code
        self.is_edit       = is_edit

        self.__setup_ui()
        self.__signals()
        self.__check_accept_disabled()

    def __setup_ui(self):

        title = QLabel("ویرایشگر اطلاعات")
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()

        self.name_edit = QLineEdit(self.fname)
        self.account_pass_edit = QLineEdit()
        self.cash_pass_edit = QLineEdit()
        self.level_selector = LevelSelector()
        self.level_selector.set_level(self.level)
        self.bale_id_edit = QLineEdit(self.bale_id)

        grid.addWidget(self.name_edit,0,0)
        grid.addWidget(QLabel("نام"),0,1)

        grid.addWidget(self.account_pass_edit,1,0)
        grid.addWidget(QLabel("پسوورد اکانت"),1,1)

        grid.addWidget(self.cash_pass_edit,2,0)
        grid.addWidget(QLabel("پسوورد صندوق"),2,1)

        grid.addWidget(self.level_selector,3,0)
        grid.addWidget(QLabel("سطح پرسنل"),3,1)

        grid.addWidget(self.bale_id_edit,4,0)
        bale_id_lbl = QLabel("Bale ID")
        bale_id_lbl.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        grid.addWidget(bale_id_lbl ,4,1)

        if self.is_edit:
            code_lbl = QLabel(self.code)
            code_lbl.setObjectName("code")
            code_lbl.setAlignment(Qt.AlignLeft)
            grid.addWidget(code_lbl,5,0)
            grid.addWidget(QLabel("کد پرسنلی"),5,1)

        self.image_lbl = QLabel()
        self.image_lbl.setObjectName('face-id')
        self.image_lbl.setFixedSize(150, 200)
        self.image_lbl.setAlignment(Qt.AlignCenter)

        pix = QPixmap(os.path.join(self.__BASE_DIR, '..', 'static', 'faces', self.face_id)).scaled(
                150,
                200,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        self.image_lbl.setPixmap(pix)
        face_img_layout = QVBoxLayout()
        face_img_layout.addWidget(self.image_lbl)

        self.cancel_btn = QPushButton("لغو")
        self.save_btn = QPushButton("ذخیره تغییرات")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)

        body_layout = QHBoxLayout()
        body_layout.addLayout(grid)
        body_layout.addLayout(face_img_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(body_layout)
        main_layout.addLayout(btn_layout)

    def __signals(self):
        self.image_lbl.mousePressEvent = self.__choose_image
        self.bale_id_edit.textChanged.connect(lambda text: self.__changed_number(self.bale_id_edit, text))
        self.cash_pass_edit.textChanged.connect(lambda text: self.__changed_number(self.cash_pass_edit, text))
        self.accepted.connect(self.__on_accept)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)

        self.name_edit.textChanged.connect(self.__check_accept_disabled)
        self.account_pass_edit.textChanged.connect(self.__check_accept_disabled)
        self.cash_pass_edit.textChanged.connect(self.__check_accept_disabled)
        self.bale_id_edit.textChanged.connect(self.__check_accept_disabled)

    def __choose_image(self, event):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select face ID",
            os.path.join(os.path.expanduser("~"), "Pictures"),
            "Images (*.jpg *.png)"
        )
        if file:
            self.face_id = file
            pix = QPixmap(file).scaled(
                self.image_lbl.width(),
                self.image_lbl.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_lbl.setPixmap(pix)

    def __changed_number(self,line_edit, text):
        text = text or '0'

        if text:
            if text[-1] in digits:
                echo = int(text)
            else:
                echo = int(text[:-1] or 0)
        else:
            echo = 0

        line_edit.setText(f"{abs(echo) or ''}")

    def __on_accept(self):
        self.fname = self.name_edit.text()
        self.password_hash = self.account_pass_edit.text()
        self.password_cash = self.cash_pass_edit.text()
        self.level = self.level_selector.level
        self.bale_id = self.bale_id_edit.text()

    def __check_accept_disabled(self):
        self.save_btn.setDisabled(not (
            self.name_edit.text() and
            (self.account_pass_edit.text() and self.cash_pass_edit.text()
            or self.is_edit)
        ))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dlg = PersonnelEditorDialog(is_edit=True, code="salkdfjdkl")
    if dlg.exec_() == QDialog.Accepted:
        print(f"fname         : {dlg.fname}")
        print(f"face_id       : {os.path.basename(dlg.face_id)}")
        print(f"passowrd hash : {dlg.password_hash}")
        print(f"password cash : {dlg.password_cash}")
        print(f"Level         :  {dlg.level}")
        print(f"Bale id       : {dlg.bale_id}")
        print(f"Code          : {dlg.code}")
    else:
        print("canceled!")

    sys.exit(0)
