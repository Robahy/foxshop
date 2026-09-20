from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import crud_customer as crud
from app.schemas import CustomerCreate, CustomerUpdate, CustomerOut

router = APIRouter(
    prefix='/customer',
    tags=['Customer']
)

# customer get by card id
@router.get('/{customer_id}', response_model=CustomerOut, status_code=status.HTTP_200_OK)
def show_customer(card_id: int, db: Session = Depends(get_db)):
    customer = crud.customer_get_by_card_id(db, card_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer {card_id} Not Found")
    return customer

# customer get by bale id
@router.get('/{bale_id}', response_model=CustomerOut, status_code=status.HTTP_200_OK)
def show_customer(bale_id: int, db: Session = Depends(get_db)):
    customer = crud.customer_get_by_bale_id(db, bale_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer {bale_id} Not Found")
    return customer

# customer create
@router.post('/', response_model=CustomerOut)
def create_customer(customer: CustomerCreate,db: Session = Depends(get_db)):
    customer = crud.create_customer(db, customer)
    if not customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return customer

@router.put('/', response_model=CustomerOut, status_code=status.HTTP_200_OK)
def update_customer(update_customer: CustomerUpdate, db: Session = Depends(get_db)):
    customer = crud.update_customer(db, update_customer)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"personnel {update_customer.id} Not Found")
    return customer