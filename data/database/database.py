from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..models.base import Base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:pass@localhost:5432/ims"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # automatically checks stale connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
