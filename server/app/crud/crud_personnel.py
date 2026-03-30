from sqlalchemy.orm import Session
from app.models import Personnel
from app.schemas import PersonnelCreate, PersonnelUpdate
from app.utils.log_decorator import log

@log
def create_personnel(db: Session, personnel: PersonnelCreate) -> Personnel:
    """
    Create New Personnel
    """
    new_personnel = Personnel(
        fname = personnel.fname,
        code = personnel.code,
        password_hash = personnel.password_hash,
        password_cach = personnel.password_cach,
        level         = personnel.level,
        bale_id       = personnel.bale_id
    )
    db.add(new_personnel)
    db.commit()
    db.refresh(new_personnel)
    return new_personnel

@log
def personnel_get_all(db: Session):
    """
    Get Personnel ALL
    """
    return db.query(Personnel).all()

@log
def personnel_cach_get_all(db: Session):
    """
    Get PersonnelCash ALL
    """
    return db.query(Personnel).filter(Personnel.level >= 2).all()

@log
def personnel_supervisor_get_all(db: Session):
    """
    Get PersonnelSupervisor ALL
    """
    return db.query(Personnel).filter(Personnel.level >= 3).all()

@log
def personnel_manager_bale_id_get_all(db: Session):
    """
    Get PersonnelSupervisor is manager bale ALL
    """
    return [i.bale_id for i in db.query(Personnel).filter(Personnel.level >= 3).filter(Personnel.bale_id != "").all()]

@log
def personnel_get_by_id(db: Session, id: int):
    """
    Get Personnel by id
    """
    return db.get(Personnel, id) or False

@log
def personnel_update_by_id(db: Session, update_personnel: PersonnelUpdate):
    """
    Update Personnel by id
    """
    personnel = db.get(Personnel, update_personnel.id)
    if not personnel:
        return False
    
    personnel.fname         = update_personnel.fname
    personnel.password_hash = update_personnel.password_hash
    personnel.password_cach = update_personnel.password_cach
    personnel.level         = update_personnel.level
    
    db.commit()
    db.refresh(personnel)
    return personnel

@log
def personnel_delete_by_id(db: Session, id: int):
    personnel = db.get(Personnel, id)
    if not personnel:
        return False
    
    db.delete(personnel)
    db.commit()
    return personnel