from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QPushButton, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from dialogs import YesNoDialog, PersonnelEditorDialog
import sys, os, shutil

class ProductsTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__DIR_FACES = os.path.join(BASE_DIR, '..', 'static', 'faces')

        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "شماره سطر",
            "عکس پرسنلی",
            "نام",
            "کد پرسنلی",
            "سمت",
            "Bale ID"
        ])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.setAlternatingRowColors(True)                       # Alternationg
        self.setEditTriggers(QTableWidget.NoEditTriggers)        # No Edit
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row Select
        self.setSelectionMode(QAbstractItemView.SingleSelection) # Single Select
        self.verticalHeader().setVisible(False)                  # Hiden Number Row
        self.setFocusPolicy(Qt.StrongFocus)                      # Select

    def reload(self,my_personnel, scrool_to_buttom: bool = False):
        scroll_pos = self.verticalScrollBar().value()
        selected = self.currentRow()

        self.setRowCount(0)
        for data in my_personnel:
            self.__add_item(data)
        
        if scrool_to_buttom:
            self.scrollToBottom()
        else:
            self.verticalScrollBar().setValue(scroll_pos)

        if selected != -1:
            self.setCurrentCell(selected, 0)

    def __add_item(self, data):
        row = self.rowCount()
        self.insertRow(row)
        level = data.get('level')
        match level:
            case 1:
                level = "normal"
            case 2:
                level = "cash"
            case 3:
                level = "supervisor"
            case 4:
                level = "manager"
        data = [
            row+1,
            data.get('face_id'),
            data.get('fname'),
            data.get('code'),
            level,
            data.get('bale_id')
        ]

        for col, value in enumerate(data):
            if col == 1:
                # PIC Personnel
                face_pic = QPixmap(os.path.join(self.__DIR_FACES, value))
                if face_pic.isNull():
                    face_pic = QPixmap(os.path.join(self.__DIR_FACES, 'base.jpg'))
                lbl = QLabel()
                lbl.setPixmap(face_pic.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                lbl.setAlignment(Qt.AlignCenter)
                self.setCellWidget(row, 1, lbl)
            else:
                item = QTableWidgetItem(str(value))
                if col != 2:
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.setItem(row, col, item)

class PersonnelManagerPage(QWidget):
    def __init__(self, changer_page, foxapi):
        super().__init__()

        self.setWindowTitle("Product Manager")

        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__DIR_FACES = os.path.join(self.__BASE_DIR, '..', 'static', 'faces')

        self.__changer_page = changer_page
        self.__foxapi = foxapi
        self.my_personnels = []

        os.makedirs(self.__DIR_FACES, exist_ok=True)
        self.__setup_ui()
        self.__signals()
        self.__check_btn_disabled()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'personnel_manager_page.qss'), 'r') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

        self.showFullScreen()

    def __setup_ui(self):
        root = QVBoxLayout(self)

        self.__table = ProductsTableWidget()
        root.addWidget(self.__table)

        # buttons
        btns = QHBoxLayout()

        self.__btn_exit = QPushButton("خروج")
        self.__btn_delete = QPushButton("حذف پرسنل")
        self.__btn_edit = QPushButton("ویرایش اطلاعات")
        self.__btn_add = QPushButton("پرسنل جدید")

        btns.addStretch()
        btns.addWidget(self.__btn_exit)
        btns.addWidget(self.__btn_delete)
        btns.addWidget(self.__btn_edit)
        btns.addWidget(self.__btn_add)
        btns.addStretch()

        root.addLayout(btns)

    def __signals(self):
        self.__table.itemClicked.connect(self.__check_btn_disabled)
        self.__btn_exit.clicked.connect(lambda: self.__changer_page.setCurrentIndex(0))
        self.__btn_delete.clicked.connect(self.__personnel_delete_signal)
        self.__btn_add.clicked.connect(self.__personnel_add_signal)
        self.__btn_edit.clicked.connect(self.__personnel_edit_signal)

    def showEvent(self, event):
        super().showEvent(event)
        self.my_personnels = self.__foxapi.get_personnels()
        self.__table.reload(self.my_personnels)

    def __personnel_add_signal(self):
        try:
            in_p = PersonnelEditorDialog()
            # file_name = 
            if in_p.exec_() == QDialog.Accepted:
                personnel = {
                    'fname'  : in_p.fname,
                    'face_id' : os.path.basename(in_p.face_id),
                    'code'     : in_p.code,
                    'password_hash' : in_p.password_hash,
                    'password_cash' : in_p.password_cash,
                    'level'         : in_p.level,
                    'bale_id'       : in_p.bale_id
                }
                res = self.__foxapi.create_personnel(personnel)
                if res.status_code == 201:
                    personnel = res.json()
                    shutil.copy(in_p.face_id, os.path.join(self.__DIR_FACES, personnel.get('face_id')))
                    self.my_personnels.append(personnel)
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_personnels)
            self.__check_btn_disabled()

    def __personnel_delete_signal(self):
        try:
            row = self.__table.currentRow()
            if row != -1:
                personnel = self.my_personnels[row]
                yes_no = YesNoDialog(f"آیا میخواهید {personnel.get('fname')} حذف شود؟")
                if yes_no.exec_() == QDialog.Accepted:
                    res = self.__foxapi.delete_personnel_by_id(personnel.get('id'))
                    if res.status_code == 204:
                        os.remove(os.path.join(self.__DIR_FACES, personnel.get('face_id')))
                        self.my_personnels.pop(row)
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_personnels)
            self.__check_btn_disabled()

    def __personnel_edit_signal(self):
        try:
            row = self.__table.currentRow()
            if row != -1:
                personnel:dict = self.my_personnels[row]
                in_p = PersonnelEditorDialog(
                    fname         = personnel.get('fname'),
                    face_id       = personnel.get('face_id'),
                    code          = personnel.get('code'),
                    level         = personnel.get('level'),
                    bale_id       = personnel.get('bale_id'),
                    is_edit       = True
                )
                if in_p.exec_() == QDialog.Accepted:
                    update_personnel = {
                        'id'            : personnel.get('id'),
                        'fname'         : in_p.fname,
                        'face_id'       : os.path.basename(in_p.face_id),
                        'code'          : in_p.code,
                        'password_hash' : in_p.password_hash or personnel.get('password_hash'),
                        'password_cash' : in_p.password_cash or personnel.get('password_cash'),
                        'level'         : in_p.level,
                        'bale_id'       : in_p.bale_id
                    }
                    res = self.__foxapi.edit_personnel_by_id(update_personnel)
                    if res.status_code == 200:
                        update_personnel = res.json()
                        if personnel.get('face_id') != update_personnel.get('face_id'):
                            os.remove(os.path.join(self.__DIR_FACES, personnel.get('face_id')))
                            shutil.copy(in_p.face_id, os.path.join(self.__DIR_FACES, personnel.get('face_id')))
                        self.my_personnels[row] = update_personnel
        except Exception:
            pass
        finally:
            self.__table.reload(self.my_personnels)
            self.__check_btn_disabled()

    def __check_btn_disabled(self):
        row_selected    = self.__table.currentRow()

        if row_selected != -1:
            self.__btn_delete.setDisabled(False)
            self.__btn_edit.setDisabled(False)
        else:
            self.__btn_delete.setDisabled(True)
            self.__btn_edit.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = PersonnelManagerPage()
    w.show()

    sys.exit(app.exec_())