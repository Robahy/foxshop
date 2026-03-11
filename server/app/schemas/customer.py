from pydantic import BaseModel, Field
from .factor import FactorOut
from typing import List

class CustomerBase(BaseModel):
    number: str = Field(
        title="NUMBER",
        description="Telefon Number",
        alias="Number",
        examples="09123456789",
        pattern="^\d$",
    )
    card_id: List[str] = Field(
        title="CARD ID",
        description="id card",
        alias="Card ID",
        examples="603720938428",
        pattern="^\d$",
    )

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    id: int
    card_id: str = Field(
        title="CARD ID",
        description="id card",
        alias="Card ID",
        examples="603720938428",
        pattern="^\d$",
    )

class CustomerOut(CustomerBase):
    id: int
    number: str
    
    factors: List[FactorOut]
    class Config:
        from_attributes = True