import requests, subprocess, os

class ServerManager:
    def __init__(self):
        self.process = None
        self.app_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'main.py')

    def start(self):
        if self.process is None:
            self.process = subprocess.Popen(
                ["python", "-m", "fastapi", "dev", self.app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None

    def is_running(self):
        return self.process is not None

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