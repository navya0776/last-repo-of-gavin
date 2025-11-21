from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date
from typing import Optional


class Demand(Base):
    __tablename__ = "Demand_table"

    eqpt_code: Mapped[str] = mapped_column(
        String, ForeignKey("equipments.eqpt_code"), nullable=False
    )

    demand_no: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    demand_type: Mapped[str] = mapped_column(
        Enum("APD", "SPD", name="dmd_type_enum"), nullable=False
    )

    eqpt_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("equipments.equipment_name"), nullable=False
    )

    fin_year: Mapped[str] = mapped_column(
        String(9), nullable=False, index=True, doc="Financial year in format YYYY-YYYY"
    )

    # existing / previously present fields
    demand_auth: Mapped[Optional[str]] = mapped_column(String(100))
    full_received: Mapped[int] = mapped_column(Integer, default=0)
    part_received: Mapped[int] = mapped_column(Integer, default=0)
    outstanding: Mapped[int] = mapped_column(Integer, default=0)
    percent_received: Mapped[float] = mapped_column(Float, default=0.0)
    remarks: Mapped[Optional[str]] = mapped_column(String(255))

    # Store / Unit details
    store_code: Mapped[str | None] = mapped_column(String(20))
    make: Mapped[str | None] = mapped_column(String(50))
    scale_or_ssg_ref: Mapped[str | None] = mapped_column(String(50))

    # Date ranges
    ap_demand_date_from: Mapped[date | None] = mapped_column(Date)
    ap_demand_date_to: Mapped[date | None] = mapped_column(Date)

    consumption_pattern_from: Mapped[date | None] = mapped_column(Date)
    consumption_pattern_to: Mapped[date | None] = mapped_column(Date)

    demand_range_from: Mapped[int | None] = mapped_column(Integer)
    demand_range_to: Mapped[int | None] = mapped_column(Integer)

    # Counts displayed in UI
    no_of_apd_demand_placed: Mapped[int] = mapped_column(Integer, default=0)
    no_of_apd_completed: Mapped[int] = mapped_column(Integer, default=0)
    no_of_eopt_for_spares: Mapped[int] = mapped_column(Integer, default=0)
    no_of_eopt_outs_for_repair: Mapped[int] = mapped_column(Integer, default=0)

    # Dropdowns / Selects
    depot: Mapped[str | None] = mapped_column(String(50))
    city: Mapped[str | None] = mapped_column(String(50))
    prefix: Mapped[str | None] = mapped_column(String(30))

    # Ledger / Scale fields
    oh_scale_ssg: Mapped[bool] = mapped_column(Boolean, default=False)
    demand_index_ledger_page: Mapped[bool] = mapped_column(Boolean, default=False)
    demand_index_oh_scale: Mapped[bool] = mapped_column(Boolean, default=False)
    demand_index_demand_no: Mapped[bool] = mapped_column(Boolean, default=False)

    # Demand type options
    is_adv_prov_demand: Mapped[bool] = mapped_column(Boolean, default=False)
    is_supplementary_demand: Mapped[bool] = mapped_column(Boolean, default=False)
    consumtion_for_the_year: Mapped[int] = mapped_column(Integer, default=0)

    # Selection options
    is_all_scaled_items: Mapped[bool] = mapped_column(Boolean, default=False)
    is_on_selection: Mapped[bool] = mapped_column(Boolean, default=False)

    # Additional fields observed from UI
    ahq_sr: Mapped[str | None] = mapped_column(String(10))
    section: Mapped[str | None] = mapped_column(String(50))
    ledger_code: Mapped[str | None] = mapped_column(String(50))
    ledger_name: Mapped[str | None] = mapped_column(String(100))

    date_of_issue: Mapped[date | None] = mapped_column(Date)
    scale_issue_no: Mapped[str | None] = mapped_column(String(50))

    # soft relationship to equipment table (no FK)
    equipment = relationship(
        "Equipment",
        primaryjoin="foreign(Demand.eqpt_code) == Equipment.eqpt_code",
        back_populates="demands",
        viewonly=True,
    )


class Dmd_junction(Base):
    __tablename__ = "demand_junc_ledger"

    Page_no: Mapped[str] = mapped_column(
        String(20), ForeignKey("ledger.ledger_page"), nullable=False, primary_key=True
    )

    demand_no: Mapped[int] = mapped_column(
        Integer, ForeignKey("Demand_table.demand_no"), nullable=False
    )

    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False)

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

    dmd_ledgers: Mapped["Ledger"] = relationship(
        "Ledger", back_populates="ledger_dmd", foreign_keys=[Page_no]
    )

    demand: Mapped["Demand"] = relationship(
        "Demand", back_populates="dmd_details", foreign_keys=[demand_no]
    )
