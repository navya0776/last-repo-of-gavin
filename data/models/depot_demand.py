from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Equipment(Base):

    __tablename__ = "eqpt_table"

    eqpt_code: Mapped[str] = mapped_column(String, primary_key=True,
                                           nullable=False)
    eqpt_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    Ledger_code: Mapped[int] = mapped_column(String(4),
                                             ForeignKey("ledger.Ledger_code"),
                                             nullable=False,
                                             unique=True)

    ledger: Mapped[list["Ledger"]] = relationship("Ledger",
                                                  back_populates="eqpt")

    dmd: Mapped[list["Demand"]] = relationship("Demand",
                                               back_populates="eqpt",
                                               cascade="all, delete")


class Demand(Base):
    __tablename__ = "Demand_table"

    eqpt_code: Mapped[str] = mapped_column(
        String, ForeignKey("eqpt_table.eqpt_code"), nullable=False
    )
    demand_no: Mapped[str] = mapped_column(String(10), primary_key=True,
                                           nullable=False)
    demand_type: Mapped[Enum] = mapped_column(
        Enum("APD", "SPD", name="dmd_type_enum"), nullable=False
    )
    equipment_code: Mapped[str] = mapped_column(String(50), nullable=False)
    equipment_name: Mapped[str] = mapped_column(String(100))
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
                                             back_populates="dmd")
    dmd_details: Mapped[list["Dmd_details"]] = relationship(
        "Dmd_details",
        back_populates="demand")


class Dmd_details(Base):

    __tablename__ = "demand_details"

    Page_no: Mapped[str] = mapped_column(String(20), nullable=False,
                                         ForeignKey("ledger.ledger_page"),
                                         primary_key=True)
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
                                            back_populates="dmd_details")
