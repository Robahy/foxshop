from sqlalchemy.orm import Session
from app.models import Factor
from app.schemas import FactorCreate
from jdatetime import datetime as jdatetime



def create_factor(db: Session, factor: FactorCreate):
    """
    Create New Factor (items = 0)
    """
    jnow = jdatetime.now()
    new_factor = Factor(
        customer_id  = factor.customer_id,
        personnel_id = factor.personnel_id,
        jcreate_at   = jdatetime.utcnow(),
        code         = jnow.strftime("%Y%m%d-%H%M%S"),
        total        = 0
    )
    db.add(new_factor)
    db.commit()
    db.refresh(new_factor)
    return new_factor

def factor_change_total(db: Session, factor_id:int, total:int):
    """
    Change factor key total by factor ID
    """
    factor = db.get(Factor, factor_id)
    if not factor:
        return False
    
    factor.total = total

    db.commit()
    db.refresh(factor)
    return factor

def factor_get_all(db: Session):
    return db.query(Factor).all() or []


def factor_get_by_id(db: Session, factor_id: int):
    """
    Get Facotr by id
    """
    return db.get(Factor, factor_id) or False