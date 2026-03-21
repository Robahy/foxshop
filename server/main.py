from fastapi import FastAPI
# from app.database import Base, engine
# from app.routers import customer
# import app.models as models

# Base.metadata.create_all(bind=engine)

app = FastAPI(
              title="Fox FastAPI",
              description="This Fast-api for FOX-SHOP",
              # version='1.0.0',
            #   docs_url=False,
            #   redoc_url=False
              )

@app.get('/')
def main():
    return {'message' : 'Welcome to FOX API'}

# app.include_router(customer.router)