from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Factor(Base):
    __tablename__ = 'factors'

    id           = Column(Integer , primary_key=True, index=True)
    customer_id  = Column(Integer , ForeignKey('customers.id'), nullable=False)
    personnel_id = Column(Integer , ForeignKey('personnels.id'), nullable=False)
    create_at    = Column(DateTime, default=datetime.utcnow)
    edit_at      = Column(DateTime, default=datetime.utcnow)
    total        = Column(Integer , nullable=False)

    customer  = relationship('Customer' , back_populates='factors')
    items     = relationship('FactorItem', back_populates='factor')
    personnel = relationship('Personnel' , back_populates='factors')

