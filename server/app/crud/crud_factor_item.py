from sqlalchemy.orm import Session
from app.models import FactorItem
from app.schemas import FactorItemCreate



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


def delete_factor_item_all(db: Session, factor_id: int):
    """
    Delete factorItem ALL
    """
    count_deleted = db.query(FactorItem).filter(FactorItem.factor_id == factor_id).delete()
    db.commit()
    return count_deleted