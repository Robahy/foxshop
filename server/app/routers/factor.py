from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas import FactorCreate, FactorOut, FactorItemCreate, FactorItemOut
from app.database import get_db
from app.crud import crud_factor, crud_factor_item
# 
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix='/factor',
    tags=['Factor']
)

@router.get('/', response_model=list[FactorItemOut], status_code=status.HTTP_200_OK)
def factor_get_all(db: Session = Depends(get_db)):
    return crud_factor.factor_get_all(db)

@router.get('/{factor_id}/', response_model=FactorItemOut, status_code=status.HTTP_200_OK)
def factor_get_by_id(factor_id:int, db:Session = Depends(get_db)):
    factor = crud_factor.factor_get_by_id(db, factor_id)
    if not factor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"factor {factor_id} NOT FOUND")
    
    factor.items
    return factor


class FactorFullCreate(BaseModel): # Funny action xD
    
    factor: FactorCreate
    items : List[FactorItemCreate]

@router.post('/', response_model=FactorOut, status_code=status.HTTP_201_CREATED)
def factor_create(full_factor: FactorFullCreate, db: Session = Depends(get_db)):
    factor = crud_factor.create_factor(db, full_factor.factor)

    total = 0
    for item in full_factor.items:
        item.factor_id = factor.id
        crud_factor_item.create_factor_item(db, item)
        total += item.total
    
    factor = crud_factor.factor_change_total(db, factor.id, total)
    return factor