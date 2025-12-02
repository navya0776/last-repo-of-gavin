from sqlalchemy import Enum, Float, ForeignKey, Integer, String,Date,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date

from .base import Base


class Demand(Base):
    __tablename__ = "Demand_table"

    # --- PRIMARY KEY ---- #
    eqpt_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # --- FOREIGN KEYS ---- #
    master_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("master_table.Master_id"), nullable=False
    )

    # --- OTHER FIELDS ---- #
    eqpt_code: Mapped[str] = mapped_column(
        String(4), nullable=False
    )

    # assumed not unique as multiple demands can be raised for same equipment
    demand_no: Mapped[int] = mapped_column(String(10),
                                           nullable=False)

    demand_type: Mapped[Enum] = mapped_column(
        Enum("APD", "SPD", name="dmd_type_enum"), nullable=False
    )

    eqpt_name: Mapped[str] = mapped_column(
        String(20), nullable=False)

    fin_year: Mapped[str] = mapped_column(
        String(9), nullable=False, index=True, doc="Financial year in format YYYY-YYYY"
    )
    dem_dt: Mapped[date] = mapped_column(Date, nullable=False)
    # existing / previously present fields
    demand_auth: Mapped[Optional[str]] = mapped_column(String(100))
    dem: Mapped[int] = mapped_column(Integer, default=0)
    full_received: Mapped[int] = mapped_column(Integer, default=0)
    no_eqpt: Mapped[int] = mapped_column(Integer, default=0)
    part_received: Mapped[int] = mapped_column(Integer, default=0)
    outstanding: Mapped[int] = mapped_column(Integer, default=0)
    percent_received: Mapped[float] = mapped_column(Float, default=0.0)
    
    is_locked: Mapped[str] = mapped_column(String(5),
                                            nullable=True)
    critical: Mapped[int] = mapped_column(Integer, default=0)
    critical_na: Mapped[int] = mapped_column(Integer, default=0)
    ved: Mapped[int] = mapped_column(Integer, default=0)
    ved_full: Mapped[int] = mapped_column(Integer, default=0)
    ved_part: Mapped[int] = mapped_column(Integer, default=0)
    ved_outstanding: Mapped[int] = mapped_column(Integer, default=0)
    ved_percent: Mapped[float] = mapped_column(Float, default=0.0)
    ved_cri: Mapped[int] = mapped_column(Integer, default=0)
    ved_cri_na: Mapped[int] = mapped_column(Integer, default=0)

    # --- RELATIONSHIPS ---- #

    eqpt: Mapped["MasterTable"] = relationship(
        "MasterTable", back_populates="dmd", uselist=False,
        foreign_keys=[master_id])

    dmd_details: Mapped[list["Dmd_junction"]] = relationship(
        "Dmd_junction", back_populates="demand"
    )


class Dmd_junction(Base):
    __tablename__ = "demand_junc_ledger"
    # ---- PRIMARY KEY ---- #
    Page_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ledger.ledger_id"), nullable=False, primary_key=True
    )
    # ---- FOREIGN KEYS ---- #
    dmd_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Demand_table.eqpt_id")
    )
    demand_no: Mapped[int] = mapped_column(Integer,
                                           nullable=False)


    Scale_no: Mapped[str] = mapped_column(String(10), nullable=False)
    Part_no: Mapped[str] = mapped_column(String(10), nullable=False)
    Nomenclature: Mapped[str] = mapped_column(String(10), nullable=False)
    A_u: Mapped[str] = mapped_column(String(10), nullable=False)
    Auth: Mapped[int] = mapped_column(Integer, nullable=False)
    Curr_stk_bal: Mapped[int] = mapped_column(Integer, nullable=False)
    Dues_in: Mapped[int] = mapped_column(Integer, nullable=False)
    Outs_Reqd: Mapped[int] = mapped_column(Integer, nullable=False)
    stk_N_yr: Mapped[int] = mapped_column(Integer, default=0)
    Reqd_as_OHS: Mapped[int] = mapped_column(Integer, default=0)
    Cons_pattern: Mapped[str] = mapped_column(String(6), default="0/0")
    qty_dem: Mapped[int] = mapped_column(Integer, default=0)
    Recd: Mapped[int] = mapped_column(Integer, default=0)
    Dept_ctrl: Mapped[str] = mapped_column(String(10), default=0)
    Dept_ctrl_dt: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # ---- RELATIONSHIPS ---- #
    dmd_ledgers: Mapped["Ledger"] = relationship(
        "Ledger", back_populates="ledger_dmd", foreign_keys=[Page_id]
    )

    demand: Mapped["Demand"] = relationship("Demand",
                                            back_populates="dmd_details",
                                            foreign_keys=[dmd_id])
