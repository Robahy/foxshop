from sqlalchemy.orm import Session
from app.models import FactorItem
from app.schemas import FactorItemCreate
from app.utils.log_decorator import log

@log
def create_factor_item(db: Session, factor_item: FactorItemCreate):
    """
    Create New Factor
    """
    new_factor_item = FactorItem(
        factor_id  = factor_item.factor_id,
        product_id = factor_item.product_id,
        price      = factor_item.price,
        off        = factor_item.off,
        no         = factor_item.no,
        total      = factor_item.total
    )

    db.add(new_factor_item)
    db.commit()
    db.refresh(new_factor_item)
    return new_factor_item

@log
def get_factor_item_all_by_factor_id(db: Session, factor_id: int):
    """
    Get FactorItem All by factor_id
    """
    return db.query(FactorItem).filter(FactorItem.factor_id == factor_id).all() or []

@log
def delete_factor_item_all(db: Session, factor_id: int):
    """
    Delete factorItem ALL
    """
    count_deleted = db.query(FactorItem).filter(FactorItem.factor_id == factor_id).delete()
    db.commit()
    return count_deleted