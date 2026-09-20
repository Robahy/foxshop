from pydantic import BaseModel, Field

class CustomerBase(BaseModel):
    number: str = Field(
        title="NUMBER",
        description="Telefon Number",
        alias="Number",
        examples="09123456789",
        pattern="^\d$",
    )
    card_id: str = Field(
        title="CARD ID",
        description="id card",
        alias="Card ID",
        examples="603720938428",
        pattern="^\d$",
    )
    bale_id: str          = Field(
        title="bale id",
        description="User ID Bale.ai",
        examples="128338497",
        default=""
    )

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    id: int

class CustomerOut(CustomerBase):
    id: int
    number: str
    bale_id: str
    class Config:
        from_attributes = True