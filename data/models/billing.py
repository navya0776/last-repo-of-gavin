from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Billing(Base):
    __tablename__ = "billing"

    # ----------- PRIMARY KEY -----------
    bill_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # ----------- FOREIGN KEYS -----------
    order_no: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_no"),
        nullable=False
    )

    ledger_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ledger.ledger_id"),
        nullable=False
    )

    # ----------- LEDGER / PART INFO -----------
    ohs_no: Mapped[str | None] = mapped_column(String(50))
    part_no: Mapped[str | None] = mapped_column(String(50))
    nomenclature: Mapped[str | None] = mapped_column(String(255))
    a_u: Mapped[str | None] = mapped_column(String(10))
    qty: Mapped[float | None] = mapped_column(Float)

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

    # ----------- BILLING AMOUNTS -----------
    rate_q: Mapped[float | None] = mapped_column(Float)
    gst_rate: Mapped[float | None] = mapped_column(Float)
    supply_qty: Mapped[float | None] = mapped_column(Float)
    amount: Mapped[float | None] = mapped_column(Float)
    gross_amt: Mapped[float | None] = mapped_column(Float)
    discount: Mapped[float | None] = mapped_column(Float)

    # ----------- RELATIONSHIPS -----------
    order: Mapped["Orders"] = relationship("Orders", back_populates="billings")
    ledger: Mapped["Ledger"] = relationship("Ledger", back_populates="ledger_billings")
