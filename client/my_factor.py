class MyFactor():
    def __init__(self,
                personnel_id: int,
                factor_id: int   = -1,
                customer_id: int = -1,
                products: list   = [],
                cash: int        = 0,
                card: int        = 0
                ):
        """
        Create A myFactor
        """
        self.__myfactor = {}
        self.reset_factor(
            factor_id    = factor_id,
            personnel_id = personnel_id,
            customer_id  = customer_id,
            products     = products,
            cash         = cash,
            card         = card
        )

    def set_factor_id(self, factor_id: int) -> bool:
        """
        Set Factor ID
        """
        try:
            self.__myfactor['factor_id'] = factor_id
        except Exception:
            return False
        return True
    
    @property
    def factor_id(self) -> int:
        """
        Get Facotr ID
        """
        return self.__myfactor.setdefault('factor_id', -1)

    def set_personnel_id(self, personnel_id: int) -> bool:
        """
        Set Personnel ID
        """
        try:
            self.__myfactor['personnel_id'] = personnel_id
        except Exception:
            return False
        return True

    @property
    def personnel_id(self) -> int:
        """
        Get Personnel ID
        """
        return self.__myfactor.setdefault('personnel_id', -1)

    def set_customer_id(self, customer_id: int) -> bool:
        """
        Set Customer ID
        """
        try:
            self.__myfactor['customer_id'] = customer_id
        except Exception:
            return False
        return True
    
    @property
    def customer_id(self) -> int:
        """
        Get Customer ID
        """
        return self.__myfactor.setdefault('customer_id', -1)

    def add_product(self, 
                    barcode:  int,
                    pname:    str,
                    price:    int,
                    off:      int,
                    num:      int  = 1,
                    removed:  bool = False
                    ) -> bool:
        """
        Add A Product to myFactor
        """
        try:
            products = self.products
            for i, product in enumerate(products):
                if not self.is_removed_product(i) and barcode == product.get('barcode'):
                    return self.set_number_product(i, -1) # Add 1 pluse num product
            # Add New Product
            products.append(
                {
                    'barcode'  : barcode,
                    'pname'    : pname,
                    'price'    : price,
                    'off'      : off,
                    'no'       : num,
                    'total'    : self.__find_total(price, off, num),
                    'removed'  : removed
                }
            )
        except Exception:
            return False
        return True

    def set_number_product(self, index: int, num: int) -> bool:
        """
        Set Number A Product (by index)\n
        for add: num = (Negative)
        """
        try:
            if self.is_removed_product(index):
                raise RuntimeError
            product = self.products[index]
            if num < 0:
                num = product.get('no') + abs(num)
            product['no'] = num
            product['total'] = self.__find_total(product.get('price'), product.get('off'), num)
        except Exception:
            return False
        return True
    
    def set_removed_product(self, index: int, is_removed: bool = True) -> bool:
        """
        Set Removed Product (by index)
        """
        try:
            self.__myfactor['products'][index]['removed'] = is_removed
        except Exception:
            return False
        return True
    
    def is_removed_product(self, index: int) -> bool:
        """
        Is Removed Product (by index)
        """
        try:
            return self.products[index].setdefault('removed', False)
        except Exception:
            return False

    @property
    def products(self) -> list:
        """
        Get All Product
        """
        return self.__myfactor.setdefault('products', [])
    
    @property
    def len_products(self) -> int:
        len_products = 0
        for i, _ in enumerate(self.products):
                if not self.is_removed_product(i):
                    len_products += 1
        return int(len_products)

    def reset_products(self, products: list = []) -> bool:
        """
        Set List Products
        """
        try:
            self.__myfactor['products'] = []
            for product in products:
                if not self.__is_product(product):
                    raise RuntimeError
                self.add_product(
                    product.get('barcode'),
                    product.get('pname'),
                    product.get('price'),
                    product.get('off'),
                    product.get('num', 1),
                    product.get('removed', False)
                )
        except Exception:
            return False
        return True

    @property
    def total(self) -> int:
        products = self.products
        total = 0
        for i, product in enumerate(products):
            if not self.is_removed_product(i):
                total += self.__find_total(product.get('price'), product.get('off'), product.get('no'))
        return int(total)
    
    @property
    def total_off(self) -> int:
        products = self.products
        total_off = 0
        for i, product in enumerate(products):
            if not self.is_removed_product(i):
                price = product.get('price')
                total_off += (price * product.get('off')/100) * product.get('no')
        return int(total_off)

    def set_payment(self, *, cash_amount=0, card_amount=0):
        """
        Set Payment
        """
        try:
            if self.total >= cash_amount + card_amount:
                self.__myfactor['cash'] = int(cash_amount)
                self.__myfactor['card'] = int(card_amount)
            else:
                raise RuntimeError
        except Exception:
            return False
        return True

    @property
    def payment_amount(self) -> dict:
        """
        Get total pyment \n
        return (chash, card)
        """
        return (
                self.__myfactor.setdefault('cash', 0),
                self.__myfactor.setdefault('card', 0)
        )
    
    @property
    def paid(self):
        """
        is paid off
        """
        return sum(self.payment_amount) >= self.total

    @property
    def balance(self):
        """
        Account Balance
        """
        return self.total - sum(self.payment_amount)

    def reset_factor(self,*,
              factor_id: int,
              personnel_id: int,
              customer_id: int,
              products: list,
              cash: int,
              card: int
            ):
        """
        Reaset myFactor
        """
        try:
            self.__myfactor = {
                "factor_id"      : factor_id,
                "personnel_id"   : personnel_id,
                "customer_id"    : customer_id,
                "products"       : products,
                "cash"           : cash,
                "card"           : card
            }
        except Exception:
            return False
        return True

    # manager functions
    def __find_total(self, price: int, off: int, num:int=1) -> int:
        """
        Find Total product
        """
        return int((price - (price * off / 100)) * num)
    
    def __is_product(self, product: dict) -> bool:
        """
        this product is product?
        """
        check = []
        try:
            if not ['barcode', 'pname', 'price', 'off'] in product.keys():
                raise RuntimeError
            check.append( str(product['barcode']).isdigit()  )
            check.append( type(product['pname']) == str()    )
            check.append( str(product['price']).isdigit()    )
            check.append( str(product['off']).isdigit() )
        except Exception:
            return False
        return all(check)

    def __str__(self):
        payment_amount = self.payment_amount
        products = self.products
        width = 100 +1
        res = ""
        res += f"\n╭{'MyFactor'.center(width-2, '─')}╮"
        res += f"\n│ {f'Factor ID      : {self.factor_id}'.ljust(width-4)} │"
        res += f"\n│ {f'Personnel ID   : {self.personnel_id}'.ljust(width-4)} │"
        res += f"\n│ {f'Customer ID    : {self.customer_id}'.ljust(width-4)} │"
        res += f"\n│ {f'Total          : {self.total}'.ljust(width-4)} │"
        res += f"\n│ {f'Total off : {self.total_off}'.ljust(width-4)} │"
        res += f"\n│ {f'Cash           : {payment_amount[0]}'.ljust(width-4)} │"
        res += f"\n│ {f'Card           : {payment_amount[1]}'.ljust(width-4)} │"
        res += f"\n│ {f'Paid           : {self.paid}'.ljust(width-4)} │"
        res += f"\n│ {f'Balance        : {self.balance}'.ljust(width-4)} │"
        res += f"\n├{'─'*(width-2)}┤"
        res += f"\n│{f"Products({len(products)})".center(width-2)}│"
        if products:
            d = (width-7)//5 +1
            res += f"\n├{'─'*d}┳{'─'*d}┳{'─'*d}┳{'─'*d}┳{'─'*d}┤"
            res += f"\n│{'Name'.center(d)}│{'Price'.center(d)}│{'Num'.center(d)}│{'off'.center(d)}│{'Total'.center(d)}│"
            res += f"\n├{'─'*d}╋{'─'*d}╋{'─'*d}╋{'─'*d}╋{'─'*d}┤"
            for i, product in enumerate(products):
                if not self.is_removed_product(i):
                    res += f"\n│{f'{product.get('pname')}'.center(d)}│{f'{product.get('price')}'.center(d)}│{f'{product.get('no')}'.center(d)}│{f'{product.get('off')}%'.center(d)}│{f'{product.get('total')}'.center(d)}│"
                    if i+1 == len(products):
                        res += f"\n├{'─'*d}┻{'─'*d}┻{'─'*d}┻{'─'*d}┻{'─'*d}┤"
                    else:
                        res += f"\n├{'─'*d}╋{'─'*d}╋{'─'*d}╋{'─'*d}╋{'─'*d}┤"
        else:
            res += f"\n│{'Nothing Product'.center(width-2)}│"
        res += f"\n│{'Foxy Shop'.center(width-2)}│"
        res += f"\n╰{'─'*(width-2)}╯"
        return res

if __name__ == "__main__":
    my_factor = MyFactor()
    my_factor.set_factor_id(5)
    my_factor.set_personnel_id(2)
    my_factor.set_customer_id(2)
    my_factor.add_product(12121212, 'gold', 200, 10,2)
    my_factor.add_product(79879877, 'car', 800, 10)
    my_factor.set_number_product(1, 20)
    my_factor.set_removed_product(0)
    my_factor.set_payment(3000, 600)
    print(my_factor)