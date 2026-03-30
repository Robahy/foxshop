import requests, subprocess, os

class ServerManager:
    def __init__(self):
        self.process = None
        self.app_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'main.py')
        self.__url = "http://127.0.0.1:8000"

    def start(self):
        if self.process is None:
            self.process = subprocess.Popen(
                [
                    "python",
                    "-u",
                    "-m",
                    "uvicorn",
                    "main:app",
                    "--app-dir",
                    os.path.dirname(self.app_path)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

    def stop(self):
        if self.process is not None:
            self.process.kill()
            self.process.wait()
            self.process = None

    def is_running(self):
        return self.process is not None
    # End FastAPI

    def get_products(self):
        try:
            res = requests.get(f'{self.__url}/product/')
            return res.json() if res.status_code == 200 else []
        except Exception:
            return []

    def get_shoper(self):
        return ["احمد محمدی", "سارا کریمی", "علی رضایی", "فاطمه نوری", "مدیریت"]

    def get_product_by_barcode(self, barcode):
        return {
            'barcode'  : barcode,
            'pname'    : 'name product',
            'price'    : 200,
            'discount' : 10,
            'no'       : 100
        }

    def verify_cashier(self, cashier_id, password) -> bool:
        return True