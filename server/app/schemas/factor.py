from pydantic import BaseModel, Field
from typing import List
from .factor_item import FactorItemOut
from datetime import datetime

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

class FactorCreate(FactorBase):
    pass

class FactorOut(FactorBase):
    id: int
    created_at: datetime
    jcreate_at: datetime
    updated_at: datetime
    code      : str
    items     : List[FactorItemOut]
    class Config:
        from_attributes = True