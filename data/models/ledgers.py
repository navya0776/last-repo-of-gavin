from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# 1️⃣ AllStores table
class AllStores(Base):
    __tablename__ = "all_stores"

    store_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    store_name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, default="Store"
    )

    # One store has many ledgers
    ledgers = relationship("Ledger", back_populates="store", cascade="all, delete")


class Ledger(Base):
    __tablename__ = "ledger"

    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("all_stores.store_id"), nullable=False
    )
    Ledger_code: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    Ledger_name: Mapped[str] = mapped_column(
        String(50), primary_key=True, nullable=False
    )

    store = relationship("AllStores", back_populates="ledgers")

    maintenance_records = relationship(
        "LedgerMaintenance", back_populates="ledger", cascade="all, delete"
    )


class LedgerMaintenance(Base):
    __tablename__ = "ledger_maintenance"

    idx: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Foreign key — links to parent Ledger
    ledger_code: Mapped[str] = mapped_column(
        String(50), ForeignKey("ledger.Ledger_code"), nullable=False
    )
    ledger_page: Mapped[str] = mapped_column(String(20), nullable=False)
    ohs_number: Mapped[str] = mapped_column(String(50))
    isg_number: Mapped[str] = mapped_column(String(50))
    ssg_number: Mapped[str] = mapped_column(String(50))
    part_number: Mapped[str] = mapped_column(String(50), nullable=False)
    nomenclature: Mapped[str] = mapped_column(String(255), nullable=False)
    a_u: Mapped[str] = mapped_column(String(10), nullable=False)
    no_off: Mapped[int] = mapped_column(Integer, nullable=False)
    scl_auth: Mapped[int] = mapped_column(Integer, nullable=False)
    unsv_stock: Mapped[int] = mapped_column(Integer, default=0)
    rep_stock: Mapped[int] = mapped_column(Integer, default=0)
    serv_stock: Mapped[int] = mapped_column(Integer, default=0)
    msc: Mapped[Enum] = mapped_column(
        Enum("M", "S", "C", name="msc_enum"), nullable=False
    )
    ved: Mapped[Enum] = mapped_column(
        Enum("V", "E", "D", name="ved_enum"), nullable=False
    )
    in_house: Mapped[Enum] = mapped_column(
        Enum("in_house", "ORD", name="in_house_enum"), nullable=False
    )
    dues_in: Mapped[int] = mapped_column(Integer)
    consumption: Mapped[int] = mapped_column(Integer)
    bin_number: Mapped[str] = mapped_column(String(50))
    group: Mapped[str] = mapped_column(String(50))
    cds_unsv_stock: Mapped[int] = mapped_column(Integer, default=0)
    cds_rep_stock: Mapped[int] = mapped_column(Integer, default=0)
    cds_serv_stock: Mapped[int] = mapped_column(Integer, default=0)
    lpp: Mapped[str] = mapped_column(String(50))
    cos_sec: Mapped[str] = mapped_column(String(50))
    cab_no: Mapped[str] = mapped_column(String(50))
    old_pg_ref: Mapped[float] = mapped_column(Float)
    Assy_Comp: Mapped[str] = mapped_column(String(50))
    Re_ord_lvl: Mapped[int] = mapped_column(Integer)
    safety_stk: Mapped[int] = mapped_column(Integer)
    lpp_dt: Mapped[str] = mapped_column(String(50))
    rate: Mapped[float] = mapped_column(Float)
    Rmks: Mapped[str] = mapped_column(String(50))

    # Relationship back to Ledger
    ledger = relationship("Ledger", back_populates="maintenance_records")
