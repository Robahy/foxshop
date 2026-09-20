from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = 'customers'

    id      = Column(Integer, primary_key=True)
    number  = Column(String, nullable=True, unique=True)
    bale_id = Column(String , default="")

    factors  = relationship('Factor', back_populates='customer')
    id_cards = relationship('CustomerCards', back_populates="customer")