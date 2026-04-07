from app.utils.security import *

def verify_pass(
    password: str       = input('Plz Enter password: '),
    plain_password: str = input('Plz Enter Plain password: ')
):
    print(verify_password(password, plain_password))

if __name__ == "__main__":
    verify_pass()