from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Personnel(Base):
    __tablename__ = 'personnels'

    id            = Column(Integer, primary_key=True, index=True)
    fname         = Column(String , nullable=False)
    code          = Column(Integer, nullable=False, unique=True)
    password_hash = Column(String , nullable=False)
    password_cach = Column(String , nullable=False)
    level         = Column(Integer, default=1)

    factors       = relationship('Factor', back_populates='personnel')