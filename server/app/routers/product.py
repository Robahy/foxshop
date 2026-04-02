from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import crud_product as crud
from app.schemas import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(
    prefix='/product',
    tags=['Product']
)

@router.get('/', response_model=list[ProductOut], status_code=status.HTTP_200_OK)
def product_get_all(db: Session = Depends(get_db)):
    return crud.product_get_all(db) or []

@router.get('/{product_barcode}', status_code=status.HTTP_200_OK)
def product_get_by_brcode(product_barcode:int, db: Session = Depends(get_db)):
    product = crud.product_get_by_barcode(db, product_barcode)
    if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_barcode} Not Found")
    return product

@router.post('/', response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def product_create(new_product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, new_product)

@router.put('/', response_model=ProductOut, status_code=status.HTTP_200_OK)
def product_update_by_id(update_product: ProductUpdate, db: Session = Depends(get_db)):
    product = crud.product_update_by_id(db, update_product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {update_product.id} Not Found")
    return product

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def product_delete_by_id(product_id: int, db: Session = Depends(get_db)):
    if not crud.product_delete_by_id(db, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {id} Not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.delete('/', status_code=status.HTTP_200_OK)
def product_delete_all(db: Session = Depends(get_db)):
    deleted_count = crud.product_delete_all(db)
    return {'deleted_count': deleted_count}
