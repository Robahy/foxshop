import requests, subprocess, os

class ServerManager:
    def __init__(self):
        self.process = None
        self.app_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'app', 'main.py')
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

    # Requests Product
    def get_products(self):
        try:
            res = requests.get(f'{self.__url}/product/')
            return res.json() if res.status_code == 200 else []
        except Exception:
            return []
        
    def get_product_by_barcode(self, barcode):
        return {
            'barcode'  : barcode,
            'pname'    : 'name product',
            'price'    : 200,
            'discount' : 10,
            'no'       : 100
        }
    
    def create_product(self, product):
        return requests.post(f"{self.__url}/product/", json=product)

    def edit_product_by_id(self, product):
        return requests.put(f"{self.__url}/product/", json=product)

    def delete_product_by_id(self, id):
        return requests.delete(f"{self.__url}/product/{id}")
    
    # Requests Personnel
    def get_personnels(self):
        try:
            res = requests.get(f'{self.__url}/personnel/')
            return res.json() if res.status_code == 200 else []
        except Exception:
            return []
        
    def create_personnel(self, personnel):
        return requests.post(f"{self.__url}/personnel/", json=personnel)
    
    def edit_personnel_by_id(self, personnel):
        return requests.put(f"{self.__url}/personnel/", json=personnel)

    def delete_personnel_by_id(self, id):
        return requests.delete(f"{self.__url}/personnel/{id}")

    def get_personnel_cash_all(self):
        try:
            res = requests.get(f'{self.__url}/personnel/cash/')
            return res.json() if res.status_code == 200 else []
        except Exception:
            return []
    
    def verify_pass_cash(self, id: int, password: str) -> bool:
        data = {
            'password': password
        }
        res = requests.post(f"{self.__url}/personnel/verify/cash/{id}", params=data)
        if res.status_code == 200:
            data = res.json()
            return data.get('is_true')
        else:
            return False
