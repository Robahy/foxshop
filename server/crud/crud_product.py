from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.utils.log_decorator import log

@log
def create_product(db: Session, product: ProductCreate) -> Product:
    """
    Create New Product
    """
    new_product = Product(
        fname   = product.fname,
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
def product_get_all(db: Session) -> list[Product]:
    return db.query(Product).all()

@log
def product_get_by_barcode(db: Session, barcode: int) -> Product | bool:
    """
    Get Product by barcode
    """
    return db.query(Product).filter(Product.barcode == barcode).first() or False

@log
def update_product(db: Session, update_product: ProductUpdate) -> Product:
    """
    Update Product by id
    """
    product = db.get(Product, update_product.id)
    if not product:
        return False
    
    product.fname   = update_product.fname
    product.price   = update_product.price
    product.off     = update_product.off
    product.no      = update_product.no
    product.barcode = update_product.barcode

    db.commit()
    db.refresh(product)
    return product

@log
def product_delete_by_id(db: Session, id: int) -> Product:
    """
    Delete Product by id
    """
    product = db.get(Product, id)

    db.delete(product)
    db.commit()
    return product

@log
def product_delete_all(db: Session) -> int:
    """
    Delete all Product by id
    """
    deleted = db.query(Product).delete()
    db.commit()
    return deleted