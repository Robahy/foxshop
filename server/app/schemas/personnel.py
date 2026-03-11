from pydantic import BaseModel, Field
from .factor import FactorOut
from typing import List

class PersonnelBase(BaseModel):
    fname: str           = Field(
        title="NAME",
        description="name personnel",
        alias="Name Personnel",
        examples="hamid",
    )
    password_hash: str   = Field(
        title="PASWORD ACCOUNT",
        description="password account",
        alias="password account",
        examples="abc_12345",
        pattern="^[A-Za-z_\d]{8,}$"
    )
    password_cach: str   = Field(
        title="PASWORD CACH",
        description="password cash",
        alias="password account",
        examples="abc_12345",
        pattern="^[A-Za-z_\d]{8,}$"
    )
    level: int           = Field(
        title="LEVEL",
        description="level personnel",
        alias="personnel level",
        examples=2,
    )

class PersonnelCreate(PersonnelBase):
    code: int            = Field(
        title="CODE",
        description="personnel code",
        alias="personnel code",
        examples=554,
    )

class PersonnelUpdate(PersonnelBase):
    id: int

class PersonnelOut(PersonnelBase):
    id: int
    code: int
    factors: List[FactorOut]
    class Config:
        from_attributes = True