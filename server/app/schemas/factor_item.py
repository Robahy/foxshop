from pydantic import BaseModel, Field


class FactorItemBase(BaseModel):
    factor_id: int  = Field(
        title="Factor ID",
        description="Factor id",
        alias="Factor id",
        examples=2,
    )
    product_id: int = Field(
        title="Product ID",
        description="procuct id",
        alias="Product id",
        examples=2,
    )
    price: int      = Field(
        title="PRICE",
        description="price product",
        alias="Price",
        examples=200-000,
    )
    off: int        = Field(
        title="off",
        description="off percent",
        alias="Percent off",
        examples=20,
    )
    no: int         = Field(
        title="number",
        description="number product",
        alias="Number",
        examples=5,
    )
    total : int     = Field(
        title="TOTAl",
        description="total",
        alias="Total",
        examples=20-000,
    )

class FactorItemCreate(FactorItemBase):
    pass

class FactorItemOut(FactorItemBase):
    id: int
    class Config:
        from_attributes = True