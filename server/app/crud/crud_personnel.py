from sqlalchemy.orm import Session
from app.models import Personnel
from app.schemas import PersonnelCreate, PersonnelUpdate

from app.utils.security import password_hash, verify_password
from datetime import datetime
import random


def create_personnel(db: Session, personnel: PersonnelCreate) -> Personnel:
    """
    Create New Personnel
    """
    last = db.query(Personnel).order_by(Personnel.id.desc()).first()
    next_id = 1 if not last else last.id + 1
    now = datetime.now()

    new_personnel = Personnel(
        fname         = personnel.fname,
        face_id       = f"{now.strftime("%Y%m%d-%H%M%S")}-{personnel.face_id}",
        code          = f"4{next_id:02}-{random.randint(1,9)}00",
        password_hash = password_hash(personnel.password_hash),
        password_cash = password_hash(personnel.password_cash),
        level         = personnel.level,
        bale_id       = personnel.bale_id
    )
    db.add(new_personnel)
    db.commit()
    db.refresh(new_personnel)
    return new_personnel


def personnel_get_all(db: Session):
    """
    Get Personnel ALL
    """
    return db.query(Personnel).all()


def personnel_cash_get_all(db: Session):
    """
    Get PersonnelCash ALL
    """
    return db.query(Personnel).filter(Personnel.level >= 2).all()


def personnel_supervisor_get_all(db: Session):
    """
    Get PersonnelSupervisor ALL
    """
    return db.query(Personnel).filter(Personnel.level >= 3).all()


def personnel_manager_bale_id_get_all(db: Session):
    """
    Get PersonnelSupervisor is manager bale ALL
    """
    return [i.bale_id for i in db.query(Personnel).filter(Personnel.level >= 3).filter(Personnel.bale_id != "").all()]


def personnel_get_by_id(db: Session, id: int):
    """
    Get Personnel by id
    """
    return db.get(Personnel, id) or False


def personnel_update_by_id(db: Session, update_personnel: PersonnelUpdate):
    """
    Update Personnel by id
    """
    personnel = db.get(Personnel, update_personnel.id)
    if not personnel:
        return False
    
    personnel.fname         = update_personnel.fname
    personnel.face_id       = update_personnel.face_id
    personnel.password_hash = password_hash(personnel.password_hash)
    personnel.password_cash = password_hash(personnel.password_cash)
    personnel.level         = update_personnel.level
    personnel.bale_id       = update_personnel.bale_id
    
    db.commit()
    db.refresh(personnel)
    return personnel


def personnel_delete_by_id(db: Session, id: int):
    personnel = db.get(Personnel, id)
    if not personnel:
        return False
    
    db.delete(personnel)
    db.commit()
    return personnel