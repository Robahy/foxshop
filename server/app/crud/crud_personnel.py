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
        level         = personnel.level
    )
    db.add(new_personnel)
    db.commit()
    db.refresonh(new_personnel)
    return new_personnel

@log
def personnel_get_by_id(db: Session, id: int) -> Personnel | bool:
    """
    Get Personnel by id
    """
    return db.get(Personnel, id) or False

@log
def update_persnnel(db: Session, update_personnel: PersonnelUpdate) -> Personnel:
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