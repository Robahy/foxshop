from sqlalchemy.orm import Session
from app.models import Customer
from app.schemas import CustomerCreate, CustomerUpdate
from app.utils.log_decorator import log

@log
def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """
    Create New Customer
    """
    new_customer = Customer(
        number  = customer.number,
        card_id = customer.card_id
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@log
def customer_get_by_card_id(db: Session, card_id: str) -> Customer | bool:
    """
    Get Customer by card id
    """
    return db.query(Customer).filter(Customer.card_id == card_id) or False

@log
def update_customer(db: Session, update_customer: CustomerUpdate) -> Customer:
    """
    Update Customer by id
    """
    customer = db.get(Customer, update_customer.id)
    if not customer:
        return False
    
    customer.card_id = update_customer.card_id
    
    db.commit()
    db.refresh(customer)
    return customer