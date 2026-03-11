from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False}) # just for sqlite3

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                            #  commit           refresh         set engine

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close
