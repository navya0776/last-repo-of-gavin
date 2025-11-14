from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Demand(Base):
    __tablename__ = "Demand_table"

    eqpt_code: Mapped[str] = mapped_column(
        String, ForeignKey("eqpt.eqpt_code"), nullable=False
    )
    demand_no: Mapped[int] = mapped_column(Integer, primary_key=True,
                                           nullable=False, autoincrement=True)
    demand_type: Mapped[Enum] = mapped_column(
        Enum("APD", "SPD", name="dmd_type_enum"), nullable=False
    )
    eqpt_name: Mapped[str] = mapped_column(
        String(11), ForeignKey("eqpt.eqpt_name"), nullable=False)
    fin_year: Mapped[str] = mapped_column(
        String(9),  # 'YYYY-YYYY' → 9 chars
        nullable=False,
        index=True,
        doc="Financial year in format YYYY-YYYY")

    demand_auth: Mapped[str | None] = mapped_column(String(100))
    full_received: Mapped[int] = mapped_column(Integer, default=0)
    part_received: Mapped[int] = mapped_column(Integer, default=0)
    outstanding: Mapped[int] = mapped_column(Integer, default=0)
    percent_received: Mapped[float] = mapped_column(Float, default=0.0)
    remarks: Mapped[str | None] = mapped_column(String(255))

    eqpt: Mapped["Equipment"] = relationship("Equipment",
                                             back_populates="dmd",
                                             uselist=False)

    dmd_details: Mapped[list["Dmd_details"]] = relationship(
        "Dmd_details",
        back_populates="demand")


class Dmd_details(Base):

    __tablename__ = "demand_details"

    Page_no: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("ledger.ledger_page"),
        nullable=False,
        primary_key=True
    )

    demand_no: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("Demand_table.demand_no"),
                                           nullable=False)

    is_locked: Mapped[bool] = mapped_column(Boolean,
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

    dmd_ledgers: Mapped["Ledger"] = relationship("Ledger",
                                                 back_populates="demand_details")

    demand: Mapped["Demand"] = relationship("Demand",
                                            back_populates="dmd_details", foreign_keys=[demand_no])
