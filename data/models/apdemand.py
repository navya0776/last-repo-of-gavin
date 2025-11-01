from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from .base import Base  # assuming you have Base = declarative_base() in base.py

class APDemand(Base):
    __tablename__ = "APDemand"

    demand_no = Column(String, primary_key=True, nullable=False)
    demand_type = Column(String(10), nullable=False)  # "APD" or "SPD"
    equipment_code = Column(String(50), nullable=False)
    equipment_name = Column(String(100), nullable=False)
    fin_year = Column(String(10), nullable=False)
    demand_auth = Column(String(100))
    depot = Column(String(100))
    prefix = Column(String(50))
    city = Column(String(100))
    full_received = Column(Integer, default=0)
    part_received = Column(Integer, default=0)
    outstanding = Column(Integer, default=0)
    percent_received = Column(Float, default=0.0)
    remarks = Column(String(255))
