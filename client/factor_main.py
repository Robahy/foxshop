import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QLineEdit, QLabel, QPushButton,
                             QGridLayout, QFrame, QSizePolicy, QSpacerItem, QHeaderView, QDialog,
                             QTableWidgetItem, QAbstractItemView, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFont, QColor
from select_shoper_dialog import SelectShoperDialog
from database import get_product_by_barcode
from my_factor import MyFactor
import winsound

class FactorTableWidget(QTableWidget):
    def __init__(self, my_factor: MyFactor):
        super().__init__()

        self.my_factor = my_factor # MyFactor

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "line",
            "Barcode", 
            "Name",
            "Price",
            "discount", 
            "number",
            "Total"
        ])

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents) 
        
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().setVisible(False)

    def reload(self) -> bool:
        """
        Update Factor
        """
        try:
            self.setRowCount(0)
            for i, data in enumerate(self.my_factor.products):
                self.__add_item(data)
                if self.my_factor.is_removed_product(i):
                    self.__set_strike_out(i)
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
                row+1,
                data.get('barcode'),
                data.get('pname'),
                data.get('price'),
                f"{data.get('discount')}%",
                data.get('no'),
                data.get('total')
            ]
            for col, value in enumerate(data):
                self.setItem(row, col, QTableWidgetItem(str(value)))
            self.scrollToBottom()
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
        
        self.__initUI()
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
            with open(".\\qss\\factor_main.qss", 'r', encoding='utf-8') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

    def __initUI(self):
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
        self.__table.setStyleSheet("font-size: 12px;")

        center_container.addWidget(self.__table, 4)

        side_panel = QFrame()
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(8, 8, 8, 8)
        side_layout.setSpacing(6)

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        side_layout.addItem(top_spacer)
        
        barcode_label = QLabel("بارکد")
        barcode_label.setStyleSheet("font-size: 0.5rem; font-weight: bold")
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
        grid.setContentsMargins(0, 0, 0, 0) # حذف حاشیه داخلی گرید

        # --- دکمه اول: بارکدهای ذخیره شده ---
        btn_saved_barcodes = QPushButton("بارکدهای ذخیره شده")
        btn_saved_barcodes.setStyleSheet("background-color: #e4f7e4; border: 1px solid #3c763d;")
        # btn_saved_barcodes.clicked.connect()
        grid.addWidget(btn_saved_barcodes, 0, 0)

        self.__btn_set_num_product = QPushButton("تعداد (F8)")
        self.__btn_set_num_product.setStyleSheet("background-color: #e4f7e4; border: 1px solid #3c763d;")
        self.__btn_set_num_product.clicked.connect(self.__set_number_item)
        grid.addWidget(self.__btn_set_num_product, 0, 1)

        # --- دکمه سوم: ابطال کالا (F10) ---
        self.__btn_cancel_item = QPushButton("ابطال کالا (F10)")
        self.__btn_cancel_item.setStyleSheet("background-color: #fce4e4; border: 1px solid #d9534f;")
        grid.addWidget(self.__btn_cancel_item, 1, 0)

        # --- دکمه دوم: ابطال فاکتور ---
        self.__btn_cancel_factor = QPushButton("ابطال فاکتور")
        self.__btn_cancel_factor.setStyleSheet("background-color: #fce4e4; border: 1px solid #d9534f;")
        grid.addWidget(self.__btn_cancel_factor, 1, 1)

        # --- دکمه چهارم: ابطال پرداخت ---
        btn_cancel_payment = QPushButton("ابطال پرداخت")
        btn_cancel_payment.setStyleSheet("background-color: #fce4e4; border: 1px solid #d9534f;")
        btn_cancel_payment.clicked.connect(lambda: self.__side_button_clicked("ابطال پرداخت"))
        grid.addWidget(btn_cancel_payment, 2, 0)

        # --- دکمه پنجم: (F2) نمایش قیمت ---
        btn_show_price = QPushButton("(F2) نمایش قیمت")
        btn_show_price.setStyleSheet("background-color: #e4f7e4; border: 1px solid #3c763d;")
        # btn_show_price.clicked.connect()
        grid.addWidget(btn_show_price, 2, 1)
        
        
        btn_show_price = QPushButton("بستن شیفت")
        btn_show_price.setStyleSheet("background-color: #fce4e4; border: 1px solid #3c763d;")
        btn_show_price.clicked.connect(self.__select_shoper)
        grid.addWidget(btn_show_price, 3, 0)


        side_layout.addLayout(grid)


        self.__exit_btn = QPushButton("خروج")
        self.__exit_btn.setObjectName("exitBtn")
        # self.exit_btn.setFixedSize(210, 45)
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

        # --- دکمه‌های پرداخت (تعریف دستی) ---
        payment_layout = QGridLayout()
        payment_layout.setSpacing(8)
        payment_layout.setContentsMargins(0, 0, 0, 0)

                # --- ردیف اول: تعریف دستی دکمه‌ها ---

        # دکمه اول ردیف اول: نقد
        btn_cash = QPushButton("نقد")
        btn_cash.setFixedHeight(50)
        btn_cash.setFont(QFont("Tahoma", 12))
        btn_cash.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;") 
        # btn_cash.clicked.connect()
        payment_layout.addWidget(btn_cash, 0, 0)

        # دکمه دوم ردیف اول: تخفیف مبلغ و کارتون
        btn_discount = QPushButton("تخفیف مبلغ و کارتون")
        btn_discount.setFixedHeight(50)
        btn_discount.setFont(QFont("Tahoma", 12))
        btn_discount.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;") 
        # btn_discount.clicked.connect()
        payment_layout.addWidget(btn_discount, 0, 1)
        
        # دکمه سوم ردیف اول: تعداد
        btn_count = QPushButton("تعداد")
        btn_count.setFixedHeight(50)
        btn_count.setFont(QFont("Tahoma", 12))
        btn_count.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;") 
        # btn_count.clicked.connect()
        payment_layout.addWidget(btn_count, 0, 2)

        # دکمه چهارم ردیف اول: پرداخت کالبرگ (ایران کیش)
        btn_kalbarg = QPushButton("پرداخت کالبرگ (ایران کیش)")
        btn_kalbarg.setFixedHeight(50)
        btn_kalbarg.setFont(QFont("Tahoma", 12))
        btn_kalbarg.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;") 
        btn_kalbarg.clicked.connect(lambda: self.__payment_button_clicked("پرداخت کالبرگ (ایران کیش)"))
        payment_layout.addWidget(btn_kalbarg, 0, 3)

        # دکمه پنجم ردیف اول: استعلام بانک‌ها
        btn_bank_inquiry = QPushButton("استعلام بانک‌ها")
        btn_bank_inquiry.setFixedHeight(50)
        btn_bank_inquiry.setFont(QFont("Tahoma", 12))
        btn_bank_inquiry.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;") 
        btn_bank_inquiry.clicked.connect(lambda: self.__payment_button_clicked("استعلام بانک‌ها"))
        payment_layout.addWidget(btn_bank_inquiry, 0, 4)


        # --- ردیف دوم: تعریف دستی دکمه‌ها ---

        # دکمه اول ردیف دوم: بانک ملی
        btn_bank_meli = QPushButton("بانک ملی")
        btn_bank_meli.setFixedHeight(50)
        btn_bank_meli.setFont(QFont("Tahoma", 12))
        btn_bank_meli.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;")
        btn_bank_meli.clicked.connect(lambda: self.__payment_button_clicked("بانک ملی"))
        payment_layout.addWidget(btn_bank_meli, 1, 0)
        
        # دکمه دوم ردیف دوم: بانک ملت
        btn_bank_mellat = QPushButton("بانک ملت")
        btn_bank_mellat.setFixedHeight(50)
        btn_bank_mellat.setFont(QFont("Tahoma", 12))
        btn_bank_mellat.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;")
        btn_bank_mellat.clicked.connect(lambda: self.__payment_button_clicked("بانک ملت"))
        payment_layout.addWidget(btn_bank_mellat, 1, 1)
        
        # دکمه سوم ردیف دوم: بانک سامان
        btn_bank_saman = QPushButton("بانک سامان")
        btn_bank_saman.setFixedHeight(50)
        btn_bank_saman.setFont(QFont("Tahoma", 12))
        btn_bank_saman.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;")
        btn_bank_saman.clicked.connect(lambda: self.__payment_button_clicked("بانک سامان"))
        payment_layout.addWidget(btn_bank_saman, 1, 2)
        
        # دکمه چهارم ردیف دوم: بانک پاسارگاد
        btn_bank_pasargad = QPushButton("بانک پاسارگاد")
        btn_bank_pasargad.setFixedHeight(50)
        btn_bank_pasargad.setFont(QFont("Tahoma", 12))
        btn_bank_pasargad.setStyleSheet("background-color: #eef2f5; border: 1px solid #bcc2ca; border-radius: 4px;")
        btn_bank_pasargad.clicked.connect(lambda: self.__payment_button_clicked("بانک پاسارگاد"))
        payment_layout.addWidget(btn_bank_pasargad, 1, 3)

        # اضافه کردن فضای خالی برای ستون پنجم ردیف دوم (برای تراز شدن با ردیف اول)
        empty_widget_r2_c4 = QWidget()
        payment_layout.addWidget(empty_widget_r2_c4, 1, 4)

        bottom_layout.addLayout(payment_layout)


        # --- نوار وضعیت ---
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(0, 5, 0, 5)
        status_layout.setSpacing(6)

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
        self.__balance_lbl.setStyleSheet("font-size: 30px;")
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
        self.__nameShoperLable.setStyleSheet("font-size: 0.7rem; color: #555;")
        footer_layout.addWidget(self.__nameShoperLable)
        
        footer_layout.addStretch()
        self.__statusLable = QLabel("Connected to store database | Suspended transactions: 0 |")
        self.__clock = QLabel("")
        self.__statusLable.setStyleSheet("font-size:0.7rem; color: #555;")
        self.__clock.setStyleSheet("font-size:0.7; color: #555;")
        footer_layout.addWidget(self.__statusLable)
        footer_layout.addWidget(self.__clock)

        bottom_layout.addLayout(footer_layout)
        
        main_layout.addWidget(bottom_frame)

    def __signals(self):
        self.__table.itemClicked.connect(self.__check_btn_disabled)
        self.__line_edit_barcode.returnPressed.connect(self.__return_peresed_line_edit)
        self.__exit_btn.clicked.connect(self.close)
        self.__btn_cancel_item.clicked.connect(self.__remove_item)
        self.__btn_cancel_factor.clicked.connect(self.__remove_factor)

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

    def __select_shoper(self):
        try:
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
        self.__add_item_by_barcode(barcode)
        self.__line_edit_barcode.setText("")

    def __add_item_by_barcode(self, barcode):
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
            winsound.MessageBeep()
            return False
        finally:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True
    
    def __set_number_item(self):
        try:
            row = self.__table.currentRow()
            if row != -1 :
                num, ok = QInputDialog.getInt(self, "set number", "Enter number", self.myfactor.products[row].get('no'))
                if ok:
                    if not self.myfactor.set_number_product(row, num):
                        raise RuntimeError
            else:
                raise RuntimeError
        except Exception as e:
            print(e)
            return False
        finally:
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
        finally:
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
        finally:
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