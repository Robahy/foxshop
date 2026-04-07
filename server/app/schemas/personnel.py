from pydantic import BaseModel, Field
from .factor import FactorOut
from typing import List

class PersonnelBase(BaseModel):
    fname: str           = Field(
        title="NAME",
        description="name personnel",
        examples="hamid",
    )
    face_id: str   = Field(
        default="base.jpg",
        title="FACE ID",
        description="Addresse photo face",
    )
    password_hash: str   = Field(
        title="PASWORD ACCOUNT",
        description="password account",
    )
    password_cash: str   = Field(
        title="PASWORD CACH",
        description="password cash",
        default=""
    )
    level: int           = Field(
        title="LEVEL",
        description="""
        level personnel
            1: base
            2: cash
            3: supervisor
            4: manager
        """,
        examples=2,
        default=1
    )
    bale_id: str          = Field(
        title="bale id",
        description="User ID Bale.ai",
        examples="128338497",
        default=""
    )

class PersonnelCreate(PersonnelBase):
    pass

class PersonnelUpdate(PersonnelBase):
    id: int

class PersonnelOut(PersonnelBase):
    id: int
    code: str
    factors: List[FactorOut]
    class Config:
        from_attributes = True

class PersonnelCachOut(BaseModel):
    id: int
    fname: str
    face_id: str
    class Config:
        from_attributes = True