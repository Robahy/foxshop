from fastapi import FastAPI
from app.database import Base, engine
import app.models as models
from app.routers import *
from app.metadata import (
    __title__,
    __description__,
    __version__
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
              title= __title__,
              description= __description__,
              version= __version__,
              # docs_url=False,
              # redoc_url=False
              )

# Include Routers
app.include_router(personnel_router)
app.include_router(product_router)
app.include_router(factor_router)
# app.include_router(customer.router)


@app.get('/')
def root():
    return {'message' : 'Welcome to FOXSHOP API'}
