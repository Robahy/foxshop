from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Factor(Base):
    __tablename__ = 'factors'

    id           = Column(Integer , primary_key=True)
    customer_id  = Column(Integer , ForeignKey('customers.id'), nullable=False)
    personnel_id = Column(Integer , ForeignKey('personnels.id'), nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)
    jcreate_at   = Column(DateTime, nullable=False)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total        = Column(Integer , nullable=False)
    is_return    = Column(Boolean, default=False)
    code         = Column(String  , nullable=False, unique=True, index=True)

    customer  = relationship('Customer'  , back_populates='factors')
    items     = relationship('FactorItem', back_populates='factor', lazy='select')
    personnel = relationship('Personnel' , back_populates='factors')