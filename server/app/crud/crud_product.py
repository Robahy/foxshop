from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.utils.log_decorator import log

@log
def create_product(db: Session, product: ProductCreate):
    """
    Create New Product
    """
    new_product = Product(
        pname   = product.pname,
        price   = product.price,
        off     = product.off,
        no      = product.no,
        barcode = product.barcode
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@log
def product_get_all(db: Session):
    """
    Product Get All
    """
    return db.query(Product).all()

@log
def product_get_by_barcode(db: Session, barcode: int):
    """
    Get Product by barcode
    """
    return db.query(Product).filter(Product.barcode == barcode).first() or False

@log
def product_update_by_id(db: Session, update_product: ProductUpdate):
    """
    Update Product by id
    """
    product = db.get(Product, update_product.id)
    if not product:
        return False
    
    product.pname   = update_product.pname
    product.price   = update_product.price
    product.off     = update_product.off
    product.no      = update_product.no

    db.commit()
    db.refresh(product)
    return product

@log
def product_delete_by_id(db: Session, id: int):
    """
    Delete Product by id
    """
    product = db.get(Product, id)
    if not product:
        return False
    
    db.delete(product)
    db.commit()
    return product

@log
def product_delete_all(db: Session) -> int:
    """
    Delete all Product by id
    """
    deleted_count = db.query(Product).delete()
    db.commit()
    return deleted_count