from fastapi import FastAPI
from app.database import Base, engine
import app.models as models
# from app.routers import customer
from app.routers import product, personnel

Base.metadata.create_all(bind=engine)

app = FastAPI(
              title="Fox FastAPI",
              description="This Fast-api for FOX-SHOP",
              version='1.0.0',
              # docs_url=False,
              # redoc_url=False
              )

# Include Routers
# app.include_router(customer.router)
app.include_router(product.router)
app.include_router(personnel.router)


@app.get('/')
def root():
    return {'message' : 'Welcome to FOXSHOP API'}
