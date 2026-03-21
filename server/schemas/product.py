from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    fname: str = Field(
        title="NAME",
        description="product name",
        alias="Name Product",
        examples="Gold",
        pattern="[^\._]+",
    )
    price: int  = Field(
        title="PRICE",
        description="price product",
        alias="Price",
        examples=200-000,
    )
    off: int    = Field(
        title="off",
        description="off percent",
        alias="Percent off",
        examples=20,
    )
    no: int     = Field(
        title="number",
        description="number product",
        alias="Number",
        examples=5,
    )
    barcode: int = Field(
        title="BARCODE",
        description="barcode product",
        alias="Barcode",
        examples=62626184333,
    )

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    id: int

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True