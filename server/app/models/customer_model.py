from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = 'customers'

    id      = Column(Integer, primary_key=True)
    card_id = Column(String, nullable=True, index=True)
    number  = Column(String, nullable=True, unique=True)

    factors = relationship('Factor', back_populates='customer')