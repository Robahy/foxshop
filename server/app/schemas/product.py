from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    pname: str = Field(
        title="NAME",
        description="product name",
        examples="Gold",
        pattern="[^\._]+",
    )
    price: int  = Field(
        title="PRICE",
        description="price product",
        examples=200000,
    )
    off: int    = Field(
        title="OFF",
        description="off percent",
        examples=20,
    )
    no: int     = Field(
        title="NUMBER",
        description="number product",
        examples=5,
    )

class ProductCreate(ProductBase):
    barcode: int = Field(
        title="BARCODE",
        description="barcode product",
        examples=62626184333,
    )

class ProductUpdate(ProductBase):
    id: int

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True