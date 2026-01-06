from sqlalchemy import Integer, String, Date, ForeignKey, select, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from .base import Base


class Inspection(Base):
    __tablename__ = "inspection"

    inspection_id: Mapped[str] = mapped_column(String(30), primary_key=True)

    ledger_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ledger.ledger_id"), nullable=False
    )

    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_master.job_id"), nullable=False
    )

    order_no: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.order_no"), nullable=False
    )

    vendor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vendor_master.vendor_id"), nullable=False
    )

    sup1: Mapped[int | None] = mapped_column(Integer)
    rej1: Mapped[int | None] = mapped_column(Integer)
    sup2: Mapped[int | None] = mapped_column(Integer)
    rej2: Mapped[int | None] = mapped_column(Integer)
    sup3: Mapped[int | None] = mapped_column(Integer)
    rej3: Mapped[int | None] = mapped_column(Integer)
    sup4: Mapped[int | None] = mapped_column(Integer)
    rej4: Mapped[int | None] = mapped_column(Integer)
    sup5: Mapped[int | None] = mapped_column(Integer)
    rej5: Mapped[int | None] = mapped_column(Integer)
    sup6: Mapped[int | None] = mapped_column(Integer)
    rej6: Mapped[int | None] = mapped_column(Integer)
    sup7: Mapped[int | None] = mapped_column(Integer)
    rej7: Mapped[int | None] = mapped_column(Integer)
    sup8: Mapped[int | None] = mapped_column(Integer)
    rej8: Mapped[int | None] = mapped_column(Integer)

    challans: Mapped[list["Challan"]] = relationship(
        "Challan",
        back_populates="inspection",
        cascade="all, delete-orphan"
    )

class Challan(Base):
    __tablename__ = "challan"

    # ----------- PRIMARY KEY (manual entry) -----------
    challan_number: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    challan_date: Mapped[Date | None] = mapped_column(Date)

    # ----------- FOREIGN KEY -----------
    inspection_id: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("inspection.inspection_id"),
        nullable=False
    )

    # ----------- RELATIONSHIP -----------    
    inspection: Mapped["Inspection"] = relationship(
        "Inspection",
        back_populates="challans"
    )
