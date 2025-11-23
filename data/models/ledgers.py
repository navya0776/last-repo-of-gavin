from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .orders import OrderJunction


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
    ohs_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    isg_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ssg_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    part_number: Mapped[str] = mapped_column(String(50), nullable=True)
    nomenclature: Mapped[str] = mapped_column(String(255), nullable=True)
    a_u: Mapped[str] = mapped_column(String(10), nullable=True)
    no_off: Mapped[int] = mapped_column(Integer, nullable=True)
    scl_auth: Mapped[int] = mapped_column(Integer, nullable=True)
    unsv_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    rep_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    serv_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    msc: Mapped[Enum | None] = mapped_column(Enum("M", "S", "C",
                                                  name="msc_enum"), nullable=True)
    ved: Mapped[Enum | None] = mapped_column(Enum("V", "E", "D",
                                                  name="ved_enum"), nullable=True)
    in_house: Mapped[Enum | None] = mapped_column(
        Enum("in_house", "ORD", name="in_house_enum")
    )
    dues_in: Mapped[int | None] = mapped_column(Integer, nullable=True)
    consumption: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bin_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    group: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cds_unsv_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    cds_rep_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    cds_serv_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    lpp: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cos_sec: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cab_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    old_pg_ref: Mapped[float | None] = mapped_column(Float, nullable=True)
    Assy_Comp: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Re_ord_lvl: Mapped[int | None] = mapped_column(Integer, nullable=True)
    safety_stk: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lpp_dt: Mapped[str | None] = mapped_column(String(50), nullable=True)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    Rmks: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Relationship to store
    store: Mapped["Stores"] = relationship("Stores", back_populates="ledgers")
    ledger_dmd: Mapped[list["Dmd_junction"]] = relationship(
        "Dmd_junction", back_populates="dmd_ledgers", cascade="all, delete"
    )

    Eqpt: Mapped["MasterTable"] = relationship("MasterTable", back_populates="legder",
                                               foreign_keys=[Master_id])
    cds_ledger: Mapped["CdsJunction"] = relationship(
        "CdsJunction", back_populates="ledger_cds")

    ledger_lpr_junc: Mapped["LPR_Junction"] = relationship(
        "LPR_Junction", back_populates="lpr_ledger_junc")

    # Many-to-many relationship to JobMaster via association table `job_ledger`
    jobs: Mapped[list["JobMaster"]] = relationship(
        "JobMaster",
        secondary="job_ledger",
        back_populates="ledgers",
        lazy="select",
    )

    # relationship to OrderJunction
    ledger_order_items: Mapped[list["OrderJunction"]] = relationship(
    "OrderJunction",
    back_populates="ledger",
    foreign_keys=[OrderJunction.ledger_page]
    )
    
    ledger_billings: Mapped[list["Billing"]] = relationship(
    "Billing",
    back_populates="ledger",
    cascade="all, delete-orphan"
)


# Association table for many-to-many between JobMaster and Ledger
class JobLedger(Base):
    __tablename__ = "job_ledger"

    job_no: Mapped[str] = mapped_column(
        String(6),
        ForeignKey("job_master.job_no"),
        primary_key=True,
    )

    ledger_page: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("ledger.ledger_page"),
        primary_key=True,
    )
