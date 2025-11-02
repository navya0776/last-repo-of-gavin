from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


# 1️⃣ AllStores table
class AllStores(Base):
    __tablename__ = "all_stores"

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String(50), nullable=False, unique=True, default="Store")

    # One store has many ledgers
    ledgers = relationship("Ledger", back_populates="store", cascade="all, delete")


class Ledger(Base):
    __tablename__ = "ledger"

    store_id = Column(Integer, ForeignKey("all_stores.store_id"), nullable=False)
    Ledger_code = Column(Integer, primary_key=True, nullable=False)
    Ledger_name = Column(String(50), primary_key=True, nullable=False)

    store = relationship("AllStores", back_populates="ledgers")
    maintenance_records = relationship(
        "LedgerMaintenance", back_populates="ledger", cascade="all, delete"
    )


class LedgerMaintenance(Base):
    __tablename__ = "ledger_maintenance"

    idx = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign key — links to parent Ledger
    ledger_code = Column(String(50), ForeignKey("ledger.Ledger_code"), nullable=False)

    ledger_page = Column(String(20), nullable=False)
    ohs_number = Column(String(50))
    isg_number = Column(String(50))
    ssg_number = Column(String(50))
    part_number = Column(String(50), nullable=False)
    nomenclature = Column(String(255), nullable=False)
    a_u = Column(String(10), nullable=False)
    no_off = Column(Integer, nullable=False)
    scl_auth = Column(Integer, nullable=False)
    unsv_stock = Column(Integer, default=0)
    rep_stock = Column(Integer, default=0)
    serv_stock = Column(Integer, default=0)
    msc = Column(Enum("M", "S", "C", name="msc_enum"), nullable=False)
    ved = Column(Enum("V", "E", "D", name="ved_enum"), nullable=False)
    in_house = Column(Enum("in_house", "ORD", name="in_house_enum"), nullable=False)
    dues_in = Column(Integer)
    consumption = Column(Integer)
    bin_number = Column(String(50))
    group = Column(String(50))
    cds_unsv_stock = Column(Integer, default=0)
    cds_rep_stock = Column(Integer, default=0)
    cds_serv_stock = Column(Integer, default=0)
    lpp = Column(String(50))
    cos_sec: Column(String(50))
    cab_no: Column(String(50))
    old_pg_ref: Column(Float)
    Assy_Comp: Column(String(50))
    Re_ord_lvl: Column(Integer)
    safety_stk: Column(Integer)
    lpp_dt: Column(String(50))
    rate: Column(Float)
    Rmks: Column(String(50))

    # Relationship back to Ledger
    ledger = relationship("Ledger", back_populates="maintenance_records")
