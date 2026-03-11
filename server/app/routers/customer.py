from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud as crud
from app.schemas import CustomerCreate, CustomerOut

router = APIRouter(
    prefix='/customer',
    tags=['customer']
)

@router.get('/')
def main():
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not Allowed")

# customer get by card id
@router.get('/{customer_id}', response_model=CustomerOut)
def show_customer(card_id: int, db: Session = Depends(get_db)):
    customer = crud.customer_get_by_card_id(db, card_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer {card_id} Not Found")
    return customer

# customer create
@router.post('/', response_model=CustomerOut)
def create_customer(customer: CustomerCreate,db: Session = Depends(get_db)):
    customer = crud.create_customer(db, customer)
    if not customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return customer