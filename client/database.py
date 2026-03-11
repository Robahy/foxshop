import requests

def get_shoper():
    return ["احمد محمدی", "سارا کریمی", "علی رضایی", "فاطمه نوری", "مدیریت"]

def get_product_by_barcode(barcode):
    return {
        'barcode'  : barcode,
        'pname'    : 'name product',
        'price'    : 200,
        'discount' : 10,
        'no'       : 100
    }

def verify_cashier(cashier_id, password) -> bool:
    return password == '1111'

    p = get_product_by_barcode('hi')
    print(list(p.values()))