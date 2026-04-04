from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import crud_personnel as crud
from app.schemas import PersonnelCreate, PersonnelUpdate, PersonnelOut, PersonnelCachOut

router = APIRouter(
    prefix='/personnel',
    tags=['Personnel'])

@router.get('/', response_model=list[PersonnelOut], status_code=status.HTTP_200_OK)
def personnel_get_all(db: Session = Depends(get_db)):
    return crud.personnel_get_all(db) or []

@router.get('/cash/', response_model=list[PersonnelCachOut], status_code=status.HTTP_200_OK)
def personnel_cash_get_all(db: Session = Depends(get_db)):
    return crud.personnel_cash_get_all(db)

@router.get('/supervisor/', response_model=list[PersonnelOut], status_code=status.HTTP_200_OK)
def personnel_cash_get_all(db: Session = Depends(get_db)):
    return crud.personnel_supervisor_get_all(db)

@router.get('/supervisor/bale_ids/', response_model=list[int], status_code=status.HTTP_200_OK)
def personnel_cash_get_all(db: Session = Depends(get_db)):
    return crud.personnel_manager_bale_id_get_all(db)

@router.get('/{personnel_id}', response_model=PersonnelOut, status_code=status.HTTP_200_OK)
def personnel_get_by_id(personnel_id: int, db: Session = Depends(get_db)):
    personnel = crud.personnel_get_by_id(db, personnel_id)
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"personnel {personnel_id} Not Found")
    return personnel

@router.post('/',response_model=PersonnelOut, status_code=status.HTTP_201_CREATED)
def personnel_crate(new_personnel: PersonnelCreate, db: Session = Depends(get_db)):
    return crud.create_personnel(db, new_personnel)

@router.put('/', response_model=PersonnelOut, status_code=status.HTTP_200_OK)
def personnel_update_by_id(update_personnel: PersonnelUpdate, db: Session = Depends(get_db)):
    personnel = crud.personnel_update_by_id(db, update_personnel)
    if not personnel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"personnel {update_personnel.id} Not Found")
    return personnel

@router.delete('/{personnel_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(personnel_id: int, db: Session = Depends(get_db)):
    personnel = crud.personnel_delete_by_id(db, personnel_id)
    if not personnel_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"personnel {personnel_id} Not Found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)