from sqlalchemy.orm import Session
from app.models import Customer, CustomerCards
from app.schemas import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer: CustomerCreate):
    """
    Create New Customer
    """
    new_customer = Customer(
        number  = customer.number,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    new_id_card = CustomerCards(
        customer_id = new_customer.id,
        card_id = customer.card_id
    )
    return new_customer


def customer_get_by_card_id(db: Session, card_id: str):
    """
    Get Customer by card id
    """
    return db.query(Customer).filter(Customer.card_id == card_id) or False


def customer_get_by_bale_id(db: Session, bale_id: str):
    """
    Get Customer by bale id
    """
    return db.query(Customer).filter(Customer.bale_id == bale_id) or False


def update_customer(db: Session, update_customer: CustomerUpdate):
    """
    Update Customer by id
    """
    customer = db.get(Customer, update_customer.id)
    if not customer:
        return False
    
    customer.number  = update_customer.number 
    customer.card_id = update_customer.card_id
    customer.bale_id = update_customer.bale_id
    
    db.commit()
    db.refresh(customer)
    return customer