"""
    This file will be used to create the schema for your database
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

