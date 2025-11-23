from sqlalchemy import Date, Float, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date


class LPR_Junction(Base):
    __tablename__ = "lpr_junction"

    lpr_no: Mapped[str] = mapped_column(String(10), ForeignKey("lpr.lpr_no"),
                                        primary_key=True)
    ledger_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey("ledger.ledger_id"),
                                             nullable=False,
                                             primary_key=True)
    srl: Mapped[int] = mapped_column(Integer, nullable=True)
    part_no: Mapped[str] = mapped_column(String(50), nullable=True)
    ohs_no: Mapped[str] = mapped_column(String(50), nullable=True)
    nomenclature: Mapped[str] = mapped_column(String(100), nullable=True)
    au: Mapped[str] = mapped_column(String(10), nullable=True)
    qty: Mapped[int] = mapped_column(Integer, nullable=True)
    lpr_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    so_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    lpp: Mapped[int] = mapped_column(Integer, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=True)
    so_no: Mapped[str] = mapped_column(String(20), nullable=True)
    so_date: Mapped[date] = mapped_column(Date, nullable=True)
    vendor: Mapped[str] = mapped_column(String(100), nullable=True)
    grp: Mapped[str] = mapped_column(String(20), nullable=True)
    lpr_date: Mapped[date] = mapped_column(Date, nullable=True)

    # ----- RELATIONSHIPS -----
    lpr: Mapped["LPR"] = relationship("LPR", back_populates="lpr_junctions")
    lpr_ledger_junc: Mapped["Ledger"] = relationship(
        "Ledger", back_populates="ledger_lpr_junc")
