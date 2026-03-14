import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QLineEdit, QLabel, QPushButton,
                             QGridLayout, QFrame, QSizePolicy, QSpacerItem, QHeaderView, QDialog,
                             QTableWidgetItem, QAbstractItemView, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFont, QColor
from dialogs.select_shoper_dialog import SelectShoperDialog
from database import get_product_by_barcode
from my_factor import MyFactor
import winsound

class FactorTableWidget(QTableWidget):
    def __init__(self, my_factor: MyFactor):
        super().__init__()

        self.my_factor = my_factor # MyFactor

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "Total",
            "number",
            "discount",
            "Price",
            "Name",
            "Barcode",
            "line"
        ])

        # width tab
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents) 
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   # Hide Scrool
        self.setShowGrid(False)                                  # Hide Grid
        self.setAlternatingRowColors(True)                       # Alternationg
        self.setEditTriggers(QTableWidget.NoEditTriggers)        # No Edit
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row Select
        self.setSelectionMode(QAbstractItemView.SingleSelection) # Single Select
        self.verticalHeader().setVisible(False)                  # Hiden Number Row
        self.setFocusPolicy(Qt.StrongFocus)                      # Select

    def reload(self, scrool_to_buttom: bool = False) -> bool:
        try:

            scroll_pos = self.verticalScrollBar().value()
            selected = self.currentRow()

            self.setRowCount(0)
            for i, data in enumerate(self.my_factor.products):
                self.__add_item(data)
                if self.my_factor.is_removed_product(i):
                    self.__set_strike_out(i)
            
            if scrool_to_buttom:
                self.scrollToBottom()
            else:
                self.verticalScrollBar().setValue(scroll_pos)

            if selected != -1:
                self.setCurrentCell(selected, 0)

        except Exception:
            return False
        return True



    def __add_item(self, data) -> bool:
        """
        Add Item
        """
        try:
            row = self.rowCount()
            self.insertRow(row)
            data = [
                data.get('total'),
                data.get('no'),
                f"{data.get('discount')}%",
                data.get('price'),
                data.get('pname'),
                data.get('barcode'),
                row+1
            ]

            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col != 4:
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.setItem(row, col, item)
        except Exception:
            return False
        return True

    def __set_strike_out(self, row):
        try:
            for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item:
                        font = item.font()
                        font.setStrikeOut(True)
                        item.setFont(font)
                        item.setBackground(QColor(240, 240, 240))
                        item.setForeground(QColor(150, 150, 150))
        except Exception:
            return False
        return True

class FactorMain(QMainWindow):
    def __init__(self,
                factor_id: int   = -1,
                personnel_id:int = -1,
                customer_id: int = -1,
                products: list   = []
        ):
        super().__init__()
        self.setWindowTitle("Fox Shoper")
        self.myfactor = MyFactor(factor_id, personnel_id, customer_id, products) # Create MyFactor
        
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__setup_ui()
        self.__load_qss()

        timer = QTimer(self)
        timer.timeout.connect(self.__update_clock)
        timer.start(1000)

        self.__signals()
        self.__check_btn_disabled()

        self.showFullScreen()
        if personnel_id == -1:
            self.__select_shoper()

    def __load_qss(self):
        """Loads stylesheets from an external QSS file."""
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'factor_main.qss'), 'r', encoding='utf-8') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

    def __setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)

        center_container = QHBoxLayout()
        main_layout.addLayout(center_container)
        self.__table = FactorTableWidget(self.myfactor)

        font = QFont("Tahoma", 11)
        self.__table.setFont(font)

        center_container.addWidget(self.__table, 4)

        side_panel = QFrame()
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(8, 8, 8, 8)
        side_layout.setSpacing(6)

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        side_layout.addItem(top_spacer)
        
        barcode_label = QLabel("بارکد")
        barcode_label.setAlignment(Qt.AlignLeft)

        self.__line_edit_barcode = QLineEdit()
        self.__line_edit_barcode.setAlignment(Qt.AlignRight)


        top_section = QFrame()
        top_layout = QVBoxLayout(top_section)
        top_layout.setSpacing(6)
        top_layout.addWidget(barcode_label)
        top_layout.addWidget(self.__line_edit_barcode)
        top_layout.addSpacing(100)

        side_layout.addWidget(top_section)

        grid = QGridLayout()
        grid.setSpacing(6)
        grid.setContentsMargins(0, 0, 0, 0)

                # گرید دکمه‌ها (تعریف دستی بدون استفاده از لیست)
        grid = QGridLayout()
        grid.setSpacing(6)
        grid.setContentsMargins(0, 0, 0, 0)

        self.__btn_saved_barcodes = QPushButton("بارکدهای ذخیره شده")
        self.__btn_saved_barcodes.setObjectName('btn-panel')
        grid.addWidget(self.__btn_saved_barcodes, 0, 0)

        self.__btn_more_option = QPushButton("سایر موارد")
        self.__btn_more_option.setObjectName('btn-panel')
        grid.addWidget(self.__btn_more_option, 0, 1)

        self.__btn_cancel_item = QPushButton("ابطال کالا (F10)")
        self.__btn_cancel_item.setObjectName('btn-panel')
        grid.addWidget(self.__btn_cancel_item, 1, 0)

        self.__btn_cancel_factor = QPushButton("ابطال فاکتور")
        self.__btn_cancel_factor.setObjectName('btn-panel')
        grid.addWidget(self.__btn_cancel_factor, 1, 1)

        self.__btn_set_num_product = QPushButton("تعداد (F8)")
        self.__btn_set_num_product.setObjectName('btn-panel')
        grid.addWidget(self.__btn_set_num_product, 2, 0)

        self.__btn_payment = QPushButton("پرداخت")
        self.__btn_payment.setObjectName('btn-panel')
        grid.addWidget(self.__btn_payment, 2, 1)
        
        self.__btn_change_shoper = QPushButton("باز/بستن شیفت")
        self.__btn_change_shoper.setObjectName('btn-panel')
        grid.addWidget(self.__btn_change_shoper, 3, 0)
        side_layout.addLayout(grid)

        btn_cancel_payment = QPushButton("ابطال پرداخت")
        btn_cancel_payment.setObjectName('btn-panel')
        grid.addWidget(btn_cancel_payment, 3, 1)

        self.__btn_show_price = QPushButton("(F2) نمایش قیمت")
        self.__btn_show_price.setObjectName('btn-panel')
        grid.addWidget(self.__btn_show_price, 4, 0)
        
        self.__btn_admin_action = QPushButton("عملیات سرپرستی")
        self.__btn_admin_action.setObjectName('btn-panel')
        grid.addWidget(self.__btn_admin_action, 4, 1)
        side_layout.addLayout(grid)

        self.__exit_btn = QPushButton("خروج")
        self.__exit_btn.setObjectName("btn-panel")
        side_layout.addWidget(self.__exit_btn)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        side_layout.addItem(bottom_spacer)

        center_container.addWidget(side_panel, 1) 

        # --- 3. بخش پایین (دکمه‌های پرداخت و وضعیت) ---
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottomStatus")
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(15, 10, 15, 15)
        bottom_layout.setSpacing(10)

        # --- نوار وضعیت ---
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(0, 5, 0, 5)
        status_layout.setSpacing(20)

        row1 = QHBoxLayout()
        row1.setSpacing(20)

        g1 = QHBoxLayout()
        lbl_rows = QLabel("تعداد سطر فاکتور")
        lbl_rows.setObjectName("statusTitle")
        self.__row_count_lbl = QLabel("0")
        self.__row_count_lbl.setObjectName("statusRes")
        self.__row_count_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g1.addWidget(lbl_rows)
        g1.addStretch(1)
        g1.addWidget(self.__row_count_lbl)
        row1.addLayout(g1)

        g2 = QHBoxLayout()
        number_product = QLabel("تعداد اقلام")
        number_product.setObjectName("statusTitle")
        self.__len_products = QLabel("0")
        self.__len_products.setObjectName("statusRes")
        self.__len_products.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g2.addWidget(number_product)
        g2.addStretch(1)
        g2.addWidget(self.__len_products)
        row1.addLayout(g2)

        g3 = QHBoxLayout()
        lbl_discount = QLabel("مجموع تخفیف")
        lbl_discount.setObjectName("statusTitle")
        self.__discount_lbl = QLabel("0")
        self.__discount_lbl.setObjectName("statusRes")
        self.__discount_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g3.addWidget(lbl_discount)
        g3.addStretch(1)
        g3.addWidget(self.__discount_lbl)
        row1.addLayout(g3)

        status_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(20)

        g4 = QHBoxLayout()
        lbl_total = QLabel("مجموع")
        lbl_total.setObjectName("statusTitle")
        self.__total_lbl = QLabel("0")
        self.__total_lbl.setObjectName("statusRes")
        self.__total_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g4.addWidget(lbl_total)
        g4.addStretch(1)
        g4.addWidget(self.__total_lbl)
        row2.addLayout(g4)

        # پرداخت
        g5 = QHBoxLayout()
        lbl_payment = QLabel("پرداخت")
        lbl_payment.setObjectName("statusTitle")
        self.__payment_lbl = QLabel("0")
        self.__payment_lbl.setObjectName("statusRes")
        self.__payment_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g5.addWidget(lbl_payment)
        g5.addStretch(1)
        g5.addWidget(self.__payment_lbl)
        row2.addLayout(g5)

        # مانده حساب (صفر بزرگ‌تر)
        g6 = QHBoxLayout()
        lbl_balance = QLabel("مانده حساب")
        lbl_balance.setObjectName("statusTitle")
        self.__balance_lbl = QLabel("0")
        self.__balance_lbl.setObjectName("statusRes")
        self.__balance_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        g6.addWidget(lbl_balance)
        g6.addStretch(1)
        g6.addWidget(self.__balance_lbl)
        row2.addLayout(g6)

        status_layout.addLayout(row2)

        bottom_layout.addLayout(status_layout)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.__nameShoperLable = QLabel("Shoper: Selecting...")
        footer_layout.addWidget(self.__nameShoperLable)
        
        footer_layout.addStretch()
        self.__statusLable = QLabel("Connected to store database | Suspended transactions: 0 |")
        self.__clock = QLabel("")
        footer_layout.addWidget(self.__statusLable)
        footer_layout.addWidget(self.__clock)

        bottom_layout.addLayout(footer_layout)
        
        main_layout.addWidget(bottom_frame)

    def __signals(self):
        self.__table.itemClicked.connect(self.__check_btn_disabled)
        self.__line_edit_barcode.returnPressed.connect(self.__return_peresed_line_edit)
        self.__exit_btn.clicked.connect(self.close)
        self.__btn_set_num_product.clicked.connect(self.__set_number_item)
        self.__btn_cancel_item.clicked.connect(self.__remove_item)
        self.__btn_cancel_factor.clicked.connect(self.__remove_factor)
        self.__btn_change_shoper.clicked.connect(self.__select_shoper)

    def __update_clock(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.__clock.setText(current_time)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2:
            print("F2")
        elif event.key() == Qt.Key_F5:
            print("F5")
        elif event.key() == Qt.Key_F8:
            self.__set_number_item()
        elif event.key() == Qt.Key_F10:
            self.__remove_item()
        else:
            super().keyPressEvent(event)

    def __select_shoper(self) -> bool:
        try:
            print('ok')
            self.__shoper = SelectShoperDialog()
            if self.__shoper.exec_() == QDialog.Accepted:
                self.myfactor.set_personnel_id(self.__shoper.id)
                self.__nameShoperLable.setText(f"Shoper: {self.__shoper.name}")
            else:
                raise RuntimeError
        except Exception:
            return False
        return True
    
    def __return_peresed_line_edit(self):
        barcode = self.__line_edit_barcode.text()
        if not self.__add_item_by_barcode(barcode):
            winsound.MessageBeep()
        self.__line_edit_barcode.setText("")

    def __add_item_by_barcode(self, barcode) -> bool:
        try:
            product = get_product_by_barcode(barcode)
            if product:
                self.myfactor.add_product(
                    product.get('barcode'),
                    product.get('pname'),
                    product.get('price'),
                    product.get('discount')
                )
            else:
                raise RuntimeError
        except Exception:
            return False
        else:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True
    
    def __set_number_item(self) -> bool:
        try:
            row = self.__table.currentRow()
            if row != -1 and not self.myfactor.is_removed_product(row):
                num, ok = QInputDialog.getInt(self, "set number", "Enter number", self.myfactor.products[row].get('no'))
                if ok:
                    if not self.myfactor.set_number_product(row, num):
                        raise RuntimeError
            else:
                raise RuntimeError
        except Exception as e:
            print(e)
            return False
        else:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True

    def __remove_item(self):
        try:
            row = self.__table.currentRow()
            if row != -1:
                if self.myfactor.is_removed_product(row):
                    if not self.myfactor.set_removed_product(row, False):
                        raise RuntimeError
                else:
                    if not self.myfactor.set_removed_product(row):
                        raise RuntimeError
            else:
                raise RuntimeError
        except Exception:
            return False
        else:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True

    def __remove_factor(self):
        try:
            reply = QMessageBox.question(self, "Remove Factor", "Are you sure remove factor?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if not self.myfactor.reset_factor():
                    raise RuntimeError
            else:
                raise RuntimeError
        except Exception:
            return False
        else:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True

    # set status
    def __reload_status(self):
        self.__row_count_lbl.setText(str(self.__table.rowCount()))
        self.__len_products.setText(str(self.myfactor.len_products))
        self.__discount_lbl.setText(str(self.myfactor.total_discount))
        self.__total_lbl.setText(str(self.myfactor.total))
        self.__payment_lbl.setText(str(sum(self.myfactor.payment_amount)))
        self.__balance_lbl.setText(str(self.myfactor.balance))

    def __check_btn_disabled(self):
        is_select_item = self.__table.currentRow() != -1
        is_item        = self.__table.rowCount()

        if is_select_item:
            self.__btn_cancel_item.setDisabled(False)
            self.__btn_set_num_product.setDisabled(False)
        else:
            self.__btn_cancel_item.setDisabled(True)
            self.__btn_set_num_product.setDisabled(True)

        if is_item:
            self.__btn_cancel_factor.setDisabled(False)
        else:
            self.__btn_cancel_factor.setDisabled(True)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FactorMain()
    window.show()

    sys.exit(app.exec_())