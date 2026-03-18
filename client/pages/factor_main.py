import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QLineEdit, QLabel, QPushButton,
                             QGridLayout, QFrame, QSizePolicy, QSpacerItem, QHeaderView, QDialog,
                             QTableWidgetItem, QAbstractItemView, QStackedWidget)
from PyQt5.QtCore import Qt, QTime, QTimer, QPropertyAnimation, QRect, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QFont, QColor
from dialogs import SelectShoperDialog, YesNoDialog, NumberDialog, CashDialog
from database import get_product_by_barcode
from my_factor import MyFactor
import winsound

class FactorTableWidget(QTableWidget):
    def __init__(self, my_factor: MyFactor):
        super().__init__()

        self.my_factor = my_factor # MyFactor

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            'Total',
            'number',
            'discount',
            'Price',
            'Name',
            'Barcode',
            'line'
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
        '''
        Add Item
        '''
        try:
            row = self.rowCount()
            self.insertRow(row)
            data = [
                data.get('total'),
                data.get('no'),
                f'{data.get('discount')}%',
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
        self.setWindowTitle('Fox Shoper')
        self.myfactor = MyFactor(factor_id, personnel_id, customer_id, products) # Create MyFactor
        
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__setup_ui()
        try:
            with open(os.path.join(self.__BASE_DIR, '..', 'qss', 'factor_main.qss'), 'r', encoding='utf-8') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            pass

        timer = QTimer(self)
        timer.timeout.connect(self.__update_clock)
        timer.start(1000)

        self.__signals()
        self.__check_btn_disabled()

        self.showFullScreen()
        if personnel_id == -1:
            self.__select_shoper_signal()
        
    def __setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Start Control Panel
        control_panel = QHBoxLayout()

        self.__table = FactorTableWidget(self.myfactor)
        font = QFont('Tahoma', 18)
        self.__table.setFont(font)

        right_panel = QFrame()
        right_panel.setObjectName('right-panel')
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 100)
        input_layout.setSpacing(6)

        lbl_barcode = QLabel('بارکد')
        lbl_barcode.setObjectName('barcode-lbl')
        lbl_barcode.setAlignment(Qt.AlignLeft)
        self.__line_edit_barcode = QLineEdit()
        self.__line_edit_barcode.setAlignment(Qt.AlignRight)

        # Btn Panel
        self.__panel_btn = QStackedWidget()

        # Menu Main
        main_menu_widget = QWidget()
        main_menu = QGridLayout(main_menu_widget)
        main_menu.setAlignment(Qt.AlignTop)
        main_menu.setSpacing(10)
        main_menu.setContentsMargins(0, 0, 0, 0)
        self.__btn_saved_barcodes = QPushButton('بارکدهای ذخیره شده')
        self.__btn_saved_barcodes.setObjectName('btn-panel')
        self.__btn_more_option = QPushButton('سایر موارد')
        self.__btn_more_option.setObjectName('btn-panel')
        self.__btn_cancel_item = QPushButton('ابطال کالا (F10)')
        self.__btn_cancel_item.setObjectName('btn-panel')
        self.__btn_cancel_factor = QPushButton('ابطال فاکتور')
        self.__btn_cancel_factor.setObjectName('btn-panel')
        self.__btn_set_num_product = QPushButton('تعداد (F8)')
        self.__btn_set_num_product.setObjectName('btn-panel')
        self.__btn_payment = QPushButton('پرداخت')
        self.__btn_payment.setObjectName('btn-panel')
        self.__btn_change_shoper = QPushButton('باز/بستن شیفت')
        self.__btn_change_shoper.setObjectName('btn-panel')
        self.__btn_cancel_payment = QPushButton('ابطال پرداخت')
        self.__btn_cancel_payment.setObjectName('btn-panel')
        self.__btn_show_price = QPushButton('(F2) نمایش قیمت')
        self.__btn_show_price.setObjectName('btn-panel')
        self.__btn_supervisor_operations = QPushButton('عملیات سرپرستی')
        self.__btn_supervisor_operations.setObjectName('btn-panel')
        self.__btn_exit = QPushButton('خروج')
        self.__btn_exit.setObjectName('btn-panel')

        # More Menu
        more_menu_widget = QWidget()
        more_menu = QGridLayout(more_menu_widget)
        more_menu.setAlignment(Qt.AlignTop)
        more_menu.setSpacing(10)
        more_menu.setContentsMargins(0, 0, 0, 0)
        self.__btn_return_factor = QPushButton('مرجوعی')
        self.__btn_return_factor.setObjectName('btn-panel')
        self.__btn_back_menu1 = QPushButton('بازگشت')
        self.__btn_back_menu1.setObjectName('btn-panel')

        # Supervisor Operations Menu
        supervisor_operations_widget = QWidget()
        supervisor_operations_menu = QGridLayout(supervisor_operations_widget)
        supervisor_operations_menu.setAlignment(Qt.AlignTop)
        supervisor_operations_menu.setSpacing(10)
        supervisor_operations_menu.setContentsMargins(0, 0, 0, 0)
        self.__btn_view_factors = QPushButton('نمایش فاکتور')
        self.__btn_view_factors.setObjectName('btn-panel')
        self.__btn_view_payments = QPushButton('نمایش فروش')
        self.__btn_view_payments.setObjectName('btn-panel')
        self.__btn_back_menu2 = QPushButton('بازگشت')
        self.__btn_back_menu2.setObjectName('btn-panel')

        bottom_spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # End control panel

        footer_layout = QVBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(20)

        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(10, 15, 10, 15)
        status_layout.setSpacing(20)

        row1 = QHBoxLayout()
        row1.setSpacing(20)
        row_count = QHBoxLayout()
        lbl_row_count = QLabel('تعداد سطر فاکتور')
        lbl_row_count.setObjectName('status-title')
        self.__lbl_row_count = QLabel('0')
        self.__lbl_row_count.setObjectName('status-res')
        self.__lbl_row_count.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        len_product = QHBoxLayout()
        lbl_len_product = QLabel('تعداد اقلام')
        lbl_len_product.setObjectName('status-title')
        self.__len_products = QLabel('0')
        self.__len_products.setObjectName('status-res')
        self.__len_products.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        discount = QHBoxLayout()
        lbl_discount = QLabel('مجموع تخفیف')
        lbl_discount.setObjectName('status-title')
        self.__lbl_discount = QLabel('0')
        self.__lbl_discount.setObjectName('status-res')
        self.__lbl_discount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        total = QHBoxLayout()
        lbl_total = QLabel('مجموع')
        lbl_total.setObjectName('status-title')
        self.__lbl_total = QLabel('0')
        self.__lbl_total.setObjectName('status-res')
        self.__lbl_total.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        payment = QHBoxLayout()
        lbl_payment = QLabel('پرداخت')
        lbl_payment.setObjectName('status-title')
        self.__lbl_payment = QLabel('0')
        self.__lbl_payment.setObjectName('status-res')
        self.__lbl_payment.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        balance = QHBoxLayout()
        lbl_balance = QLabel('مانده حساب')
        lbl_balance.setObjectName('status-title')
        self.__lbl_balance = QLabel('0')
        self.__lbl_balance.setObjectName('status-balance')
        self.__lbl_balance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Status Bar
        status_bar_panel = QFrame()
        status_bar = QHBoxLayout(status_bar_panel)
        status_bar_panel.setObjectName('status-bar')
        status_bar.setContentsMargins(0, 0, 0, 0)
        self.__nameShoperLable = QLabel('Shoper: Selecting...')
        status_bar.addWidget(self.__nameShoperLable)
        status_bar.addStretch(1)
        self.__lbl_status = QLabel('Connected to store database | Suspended transactions: 0 |')
        self.__lbl_clock = QLabel()

        # Add Total
        # Add Control Panel
        # Add input_layout
        input_layout.addWidget(lbl_barcode)
        input_layout.addWidget(self.__line_edit_barcode)
        # Add main_menu
        main_menu.addWidget(self.__btn_saved_barcodes, 0, 0)
        main_menu.addWidget(self.__btn_more_option, 0, 1)
        main_menu.addWidget(self.__btn_cancel_item, 1, 0)
        main_menu.addWidget(self.__btn_cancel_factor, 1, 1)
        main_menu.addWidget(self.__btn_set_num_product, 2, 0)
        main_menu.addWidget(self.__btn_payment, 2, 1)
        main_menu.addWidget(self.__btn_change_shoper, 3, 0)
        main_menu.addWidget(self.__btn_cancel_payment, 3, 1)
        main_menu.addWidget(self.__btn_show_price, 4, 0)
        main_menu.addWidget(self.__btn_supervisor_operations, 4, 1)
        main_menu.addWidget(self.__btn_exit, 5, 0, 1, 2)
        # Add more_menu
        more_menu.addWidget(self.__btn_return_factor, 0, 0)
        more_menu.addWidget(self.__btn_back_menu1, 0, 1)
        # Add supervisor operation panel
        supervisor_operations_menu.addWidget(self.__btn_view_factors, 0, 0)
        supervisor_operations_menu.addWidget(self.__btn_back_menu2, 0, 1)
        supervisor_operations_menu.addWidget(self.__btn_view_payments, 1, 1)
        # Add panel_btn
        self.__panel_btn.addWidget(main_menu_widget)
        self.__panel_btn.addWidget(more_menu_widget)
        self.__panel_btn.addWidget(supervisor_operations_widget)
        # Add sid_layout
        right_layout.addItem(top_spacer)
        right_layout.addLayout(input_layout)
        right_layout.addWidget(self.__panel_btn)
        right_layout.addItem(bottom_spacer)
        # Add control_panel
        control_panel.addWidget(self.__table, 8)
        control_panel.addWidget(right_panel, 2)
        # End Control Panel
        # Add Status Panel
        # Add row_count
        row_count.addWidget(lbl_row_count)
        row_count.addStretch(1)
        row_count.addWidget(self.__lbl_row_count)
        # Add len_product
        len_product.addWidget(lbl_len_product)
        len_product.addStretch(1)
        len_product.addWidget(self.__len_products)
        # Add discount
        discount.addWidget(lbl_discount)
        discount.addStretch(1)
        discount.addWidget(self.__lbl_discount)
        # Add row1
        row1.addLayout(row_count)
        row1.addLayout(len_product)
        row1.addLayout(discount)
        # Add total
        total.addWidget(lbl_total)
        total.addStretch(1)
        total.addWidget(self.__lbl_total)
        # Add payment
        payment.addWidget(lbl_payment)
        payment.addStretch(1)
        payment.addWidget(self.__lbl_payment)
        # Add balance
        balance.addWidget(lbl_balance)
        balance.addStretch(1)
        balance.addWidget(self.__lbl_balance)
        # Add row2
        row2.addLayout(total)
        row2.addLayout(payment)
        row2.addLayout(balance)
        # Add status_bar
        status_bar.addWidget(self.__lbl_status)
        status_bar.addWidget(self.__lbl_clock)
        # Add status_layout
        status_layout.addLayout(row1)
        status_layout.addLayout(row2)
        # Add footer_layout
        footer_layout.addLayout(status_layout)
        footer_layout.addWidget(status_bar_panel)
        # Add Main
        main_layout.addLayout(control_panel)
        main_layout.addLayout(footer_layout)
        # End Add
        self.setCentralWidget(central_widget)

    def __change_panel_btn(self, index):
        current = self.__panel_btn.currentWidget()
        next_w = self.__panel_btn.widget(index)

        w = self.__panel_btn.width() +10
        h = self.__panel_btn.height()

        next_w.setGeometry(w, 0, w, h)
        next_w.show()

        anim_out = QPropertyAnimation(current, b'geometry')
        anim_out.setDuration(600)
        anim_out.setStartValue(QRect(0, 0, w, h))
        anim_out.setEndValue(QRect(w, 0, w, h))
        anim_out.setEasingCurve(QEasingCurve.InOutCubic)

        anim_in = QPropertyAnimation(next_w, b'geometry')
        anim_in.setDuration(600)
        anim_in.setStartValue(QRect(w, 0, w, h))
        anim_in.setEndValue(QRect(0, 0, w, h))
        anim_in.setEasingCurve(QEasingCurve.InOutCubic)

        group = QSequentialAnimationGroup()
        group.addAnimation(anim_out)
        group.addAnimation(anim_in)

        group.finished.connect(lambda: self.__panel_btn.setCurrentIndex(index))

        self.anim = group
        group.start()

    def __signals(self):
        self.__table.itemClicked.connect(self.__check_btn_disabled)
        self.__line_edit_barcode.returnPressed.connect(self.__return_peresed_line_edit_signal)
        self.__btn_back_menu1.clicked.connect(lambda: self.__change_panel_btn(0))
        self.__btn_back_menu2.clicked.connect(lambda: self.__change_panel_btn(0))
        self.__btn_more_option.clicked.connect(lambda: self.__change_panel_btn(1))
        self.__btn_supervisor_operations.clicked.connect(lambda: self.__change_panel_btn(2))
        self.__btn_exit.clicked.connect(self.close)
        self.__btn_payment.clicked.connect(self.__cash_payment_signal)
        self.__btn_cancel_payment.clicked.connect(self.__cash_payment_cancle_signal)
        self.__btn_set_num_product.clicked.connect(self.__set_number_item_signal)
        self.__btn_cancel_item.clicked.connect(self.__remove_item_signal)
        self.__btn_cancel_factor.clicked.connect(self.__remove_factor_signal)
        self.__btn_change_shoper.clicked.connect(self.__select_shoper_signal)

    def __update_clock(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.__lbl_clock.setText(current_time)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2: 
            print('F2')
        elif event.key() == Qt.Key_F5: # cash payment
            if self.myfactor.balance:
                self.__cash_payment_signal()
        elif event.key() == Qt.Key_F8: # set number product
            self.__set_number_item_signal()
        elif event.key() == Qt.Key_F10:
            self.__remove_item_signal()
        else:
            super().keyPressEvent(event)

    def __select_shoper_signal(self) -> bool:
        try:
            self.__shoper = SelectShoperDialog()
            if self.__shoper.exec_() == QDialog.Accepted:
                self.myfactor.set_personnel_id(self.__shoper.id)
                self.__nameShoperLable.setText(f'Shoper: {self.__shoper.name}')
            else:
                raise RuntimeError
        except Exception:
            return False
        return True
    
    def __return_peresed_line_edit_signal(self):
        barcode = self.__line_edit_barcode.text()
        if not self.__add_item_by_barcode(barcode):
            winsound.MessageBeep()
        self.__line_edit_barcode.setText('')

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
        finally:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True
    
    def __set_number_item_signal(self) -> bool:
        try:
            row = self.__table.currentRow()
            if row != -1 and not self.myfactor.is_removed_product(row):
                number = NumberDialog(int(self.myfactor.products[row]['no']))
                if number.exec_() == QDialog.Accepted:
                    if not self.myfactor.set_number_product(row, number.num):
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
    
    def __cash_payment_signal(self):
        try:
            cash_number = CashDialog(self.myfactor.balance)
            if cash_number.exec_() == QDialog.Accepted:
                if not self.myfactor.set_payment(cash_amount=sum(self.myfactor.payment_amount)+cash_number.cash_num):
                    raise RuntimeError
        except Exception:
            return False
        finally:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True
    
    def __cash_payment_cancle_signal(self):
        try:
            yes_no = YesNoDialog('آیا پرداختی ها ابطال شود؟')
            if yes_no.exec_() == QDialog.Accepted:
                if not self.myfactor.set_payment(cash_amount=0, card_amount=0):
                        raise RuntimeError
        except Exception:
            return False
        finally:
            self.__table.reload()
            self.__reload_status()
            self.__check_btn_disabled()
        return True

    def __remove_item_signal(self):
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

    def __remove_factor_signal(self):
        try:
            yes_no = YesNoDialog('آیا میخواهید فاکتور حذف شود؟')
            if yes_no.exec_() == QDialog.Accepted:
                if not self.myfactor.reset_factor(
                        factor_id    = -1,
                        personnel_id = self.myfactor.personnel_id,
                        customer_id  = -1,
                        products     = [],
                        cash         = 0,
                        card         = 0
                    ):
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
        self.__lbl_row_count.setText(str(self.__table.rowCount()))
        self.__len_products.setText(str(self.myfactor.len_products))
        self.__lbl_discount.setText(f'{self.myfactor.total_discount:,}')
        self.__lbl_total.setText(f'{self.myfactor.total:,}')
        self.__lbl_payment.setText(f'{sum(self.myfactor.payment_amount):,}')
        self.__lbl_balance.setText(f'{self.myfactor.balance:,}')

    def __check_btn_disabled(self):
        row_selected    = self.__table.currentRow()

        if row_selected != -1:
            self.__btn_cancel_item.setDisabled(False)
            self.__btn_set_num_product.setDisabled(self.myfactor.is_removed_product(row_selected))
        else:
            self.__btn_cancel_item.setDisabled(True)
            self.__btn_set_num_product.setDisabled(True)

        self.__btn_cancel_factor.setDisabled(not self.__table.rowCount())
        self.__btn_payment.setDisabled(not self.myfactor.balance)
        self.__btn_cancel_payment.setDisabled(not sum(self.myfactor.payment_amount))

    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FactorMain()
    window.show()

    sys.exit(app.exec_())