from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# 1️⃣ AllStores table
class Stores(Base):
    __tablename__ = "stores"

    store_id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                          autoincrement=True)

    store_name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, default="Store"
    )

    # One store has many ledgers
    ledgers = relationship("Ledger", back_populates="store",
                           cascade="all, delete")


class Ledger(Base):
    __tablename__ = "ledger"

    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stores.store_id"), nullable=False
    )
    Master_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey(
                                               "master_table.Master_id"),
                                           nullable=False)

    Ledger_code: Mapped[str] = mapped_column(String(4),
                                             nullable=False)

    ledger_page: Mapped[str] = mapped_column(String(20), nullable=False,
                                             primary_key=True)
    ohs_number: Mapped[str | None] = mapped_column(String(50))
    isg_number: Mapped[str | None] = mapped_column(String(50))
    ssg_number: Mapped[str | None] = mapped_column(String(50))
    part_number: Mapped[str] = mapped_column(String(50), nullable=False)
    nomenclature: Mapped[str] = mapped_column(String(255), nullable=False)
    a_u: Mapped[str] = mapped_column(String(10), nullable=False)
    no_off: Mapped[int] = mapped_column(Integer, nullable=False)
    scl_auth: Mapped[int] = mapped_column(Integer, nullable=False)
    unsv_stock: Mapped[int] = mapped_column(Integer, default=0)
    rep_stock: Mapped[int] = mapped_column(Integer, default=0)
    serv_stock: Mapped[int] = mapped_column(Integer, default=0)
    msc: Mapped[Enum | None] = mapped_column(Enum("M", "S", "C",
                                                  name="msc_enum"))
    ved: Mapped[Enum | None] = mapped_column(Enum("V", "E", "D",
                                                  name="ved_enum"))
    in_house: Mapped[Enum | None] = mapped_column(
        Enum("in_house", "ORD", name="in_house_enum")
    )
    dues_in: Mapped[int | None] = mapped_column(Integer)
    consumption: Mapped[int | None] = mapped_column(Integer)
    bin_number: Mapped[str | None] = mapped_column(String(50))
    group: Mapped[str | None] = mapped_column(String(50))
    cds_unsv_stock: Mapped[int] = mapped_column(Integer, default=0)
    cds_rep_stock: Mapped[int] = mapped_column(Integer, default=0)
    cds_serv_stock: Mapped[int] = mapped_column(Integer, default=0)
    lpp: Mapped[str | None] = mapped_column(String(50))
    cos_sec: Mapped[str | None] = mapped_column(String(50))
    cab_no: Mapped[str | None] = mapped_column(String(50))
    old_pg_ref: Mapped[float | None] = mapped_column(Float)
    Assy_Comp: Mapped[str | None] = mapped_column(String(50))
    Re_ord_lvl: Mapped[int | None] = mapped_column(Integer)
    safety_stk: Mapped[int | None] = mapped_column(Integer)
    lpp_dt: Mapped[str | None] = mapped_column(String(50))
    rate: Mapped[float | None] = mapped_column(Float)
    Rmks: Mapped[str | None] = mapped_column(String(50))

    # Relationship to store
    store: Mapped["Stores"] = relationship("Stores", back_populates="ledgers")
    ledger_dmd: Mapped[list["Dmd_junction"]] = relationship(
        "Dmd_junction", back_populates="dmd_ledgers", cascade="all, delete"
    )

    Eqpt: Mapped["MasterTable"] = relationship("MasterTable", back_populates="legder",
                                               uselist=False, foreign_keys=[Master_id])
    cds_ledger: Mapped["CdsJunction"] = relationship(
        "CdsJunction", back_populates="ledger_cds")

    ledger_lpr_junc: Mapped["LPR_Junction"] = relationship(
        "LPR_Junction", back_populates="lpr_ledger_junc")
