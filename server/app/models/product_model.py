from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id      = Column(Integer, primary_key=True)
    fname   = Column(String , nullable=False, unique=True)
    price   = Column(Integer, nullable=False)
    off     = Column(Integer, nullable=False)
    no      = Column(Integer, nullable=False)
    barcode = Column(Integer, nullable=False, unique=True, index=True)