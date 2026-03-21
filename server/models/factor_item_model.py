from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class FactorItem(Base):
    __tablename__ = 'factor_items'

    id         = Column(Integer, primary_key=True, index=True)
    factor_id  = Column(Integer, ForeignKey('factors.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price      = Column(Integer, nullable=False)
    off        = Column(Integer, nullable=False)
    no         = Column(Integer, nullable=False)
    total      = Column(Integer, nullable=False)

    factor  = relationship('Factor', back_populates='items')