from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CustomerCards(Base):
    __tablename__ = "customer_cards"

    id          = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    card_id     = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="id_cards")