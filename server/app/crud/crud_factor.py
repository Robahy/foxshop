from sqlalchemy.orm import Session
from app.models import Factor, FactorItem
from app.schemas import FactorCreat, FactorItemCreate
from datetime import datetime
from app.utils.log_decorator import log

@log
def create_factor(db: Session, factor: FactorCreat):
    """
    Create New Factor (items = 0)
    """
    new_factor = Factor(
        customer_id  = factor.customer_id,
        personnel_id = factor.personnel_id,
        total        = 0
    )
    db.add(new_factor)
    db.commit()
    db.refresh(new_factor)
    return new_factor

@log
def factor_get_by_id(db: Session, id: int):
    """
    Get Facotr by id
    """
    return db.get(Factor, id) or False