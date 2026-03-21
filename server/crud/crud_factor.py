from sqlalchemy.orm import Session
from app.models import Factor, FactorItem
from app.schemas import FactorCreat, FactorItemCreate
from datetime import datetime
from app.utils.log_decorator import log

@log
def create_factor(db: Session, factor: FactorCreat) -> Factor:
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
def factor_item_delete_all(db: Session, factor_id: int) -> int:
    """
    Delete item all by factor ID
    or Restart items
    """
    factor = db.get(Factor, factor_id)
    if not factor:
        return False
    factor.total = 0

    deleted = db.query(FactorItem).filter(FactorItem.factor_id == factor_id).delete()
    db.commit()
    return deleted

@log
def factor_item_add(db: Session, item: FactorItemCreate) -> FactorItem | bool:
    """
    Add Item Factor
    """
    factor = db.get(Factor, item.factor_id)
    if not factor:
        return False
    factor.edit_at = datetime.utcnow()
    factor.total   += item.total

    new_item = FactorItem(
        factor_id  = item.factor_id,
        product_id = item.product_id,
        price      = item.price,
        off        = item.off,
        no         = item.no,
        total      = item.total
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@log
def factor_get_by_id(db: Session, id: int) -> Factor | bool:
    """
    Get Full Facotr by id
    """
    return db.get(Factor, id) or False