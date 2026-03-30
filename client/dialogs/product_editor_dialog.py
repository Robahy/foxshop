from PyQt5.QtWidgets import (
    QHBoxLayout,QPushButton, QDialog,
    QLineEdit, QSpinBox, QDoubleSpinBox, QFormLayout
)

class ProductEditDialog(QDialog):
    # سیگنالی که داده‌های ویرایش شده رو برمی‌گردونه
    product_saved = pyqtSignal(dict)

    def __init__(self, product_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ویرایش کالا" if product_data else "افزودن کالا")
        self.setMinimumWidth(400)
        self.setModal(True) # مودال باشه که مزاحم صفحه اصلی نشه

        self.product_data = product_data # اگر ویرایش باشه، داده‌های فعلی کالا
        self.is_editing = product_data is not None

        self.layout = QFormLayout(self)

        # فیلدها
        self.name_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setDecimals(2)
        self.price_input.setRange(0.00, 1000000000.00) # محدوده قیمت
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setDecimals(2)
        self.discount_input.setRange(0.00, 100.00) # درصد تخفیف
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 1000000) # محدوده تعداد
        self.barcode_input = QLineEdit()

        self.layout.addRow("نام کالا:", self.name_input)
        self.layout.addRow("قیمت کالا:", self.price_input)
        self.layout.addRow("تخفیف (%):", self.discount_input)
        self.layout.addRow("تعداد:", self.quantity_input)
        self.layout.addRow("بارکد:", self.barcode_input)

        # دکمه‌های Save/Cancel
        self.save_button = QPushButton("ذخیره")
        self.cancel_button = QPushButton("لغو")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addRow(self.button_layout)

        # اتصال سیگنال‌ها
        self.save_button.clicked.connect(self.save_product)
        self.cancel_button.clicked.connect(self.reject) # reject دیالوگ را می‌بندد

        # اگر در حالت ویرایش هستیم، فیلدها را پر کن
        if self.is_editing:
            self.name_input.setText(product_data.get('نام کالا', ''))
            self.price_input.setValue(float(product_data.get('قیمت کالا', 0.0)))
            self.discount_input.setValue(float(product_data.get('تخفیف', 0.0)))
            self.quantity_input.setValue(int(product_data.get('تعداد', 0)))
            self.barcode_input.setText(product_data.get('بارکد', ''))

    def save_product(self):
        if not self.name_input.text():
            # اینجا می‌تونی یک پیغام خطا نشون بدی
            print("نام کالا نمی‌تواند خالی باشد.")
            return

        # جمع‌آوری داده‌ها
        product_info = {
            "نام کالا": self.name_input.text(),
            "قیمت کالا": str(self.price_input.value()),
            "تخفیف": str(self.discount_input.value()),
            "تعداد": str(self.quantity_input.value()),
            "بارکد": self.barcode_input.text()
        }
        # اگر در حالت ویرایش هستیم، شماره سطر را هم اضافه می‌کنیم (که از داده‌های اصلی گرفته شده)
        if self.is_editing and 'شماره سطر' in self.product_data:
            product_info['شماره سطر'] = self.product_data['شماره سطر']
        else:
            # برای کالای جدید، شماره سطر رو فعلا خالی می‌ذاریم، بعداً در تیبل تنظیم میشه
            product_info['شماره سطر'] = ''

        self.product_saved.emit(product_info) # ارسال داده‌ها با سیگنال
        self.accept() # بستن دیالوگ با نتیجه موفق
