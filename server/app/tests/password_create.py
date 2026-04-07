from ..utils.security import *

def create_password(
    password: str = input('Plz Enter password: ')
):
    print(password_hash(password))

if __name__ == "__main__":
    create_password()