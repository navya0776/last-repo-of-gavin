from typing import Literal

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from .base import Base


class Ledger(Base):
    __tablename__ = "Ledger"
    Ledger_name = Column(Integer, primary_key=True, nullable=False)
    Ledger_code = Column(String(50), primary_key=True, nullable=False)
