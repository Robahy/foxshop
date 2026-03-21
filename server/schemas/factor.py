from pydantic import BaseModel, Field
from typing import List
from .factor_item import FactorItemOut

class FactorBase(BaseModel):
    customer_id: int = Field(
        title="Customer ID",
        description="customers id",
        alias="Customer ID",
        examples=2,
    )
    personnel_id: int = Field(
        title="Personnel ID",
        description="personnel id",
        alias="Personnel ID",
        examples=10,
    )

class FactorCreat(FactorBase):
    pass

class FactorOut(FactorBase):
    id: int
    total     : int
    items     : List[FactorItemOut]
    class Config:
        from_attributes = True