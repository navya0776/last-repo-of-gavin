from sqlalchemy import Integer, String, Boolean, Enum, Date, ForeignKey,Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from .base import Base


class Orders(Base):
    __tablename__ = "orders"

    order_no: Mapped[int] = mapped_column(Integer, primary_key=True)

    curr_indent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("floating_indent.indent_id"),
        nullable=False
    )

    curr_indent: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    order_type: Mapped[str] = mapped_column(
        Enum("MKT", "GEM", "GFR", name="order_type_enum"),
        nullable=False
    )

    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    order_date: Mapped[date | None] = mapped_column(Date)
    cancelled_date: Mapped[date | None] = mapped_column(Date)

    # correct relationship to FloatingIndent
    indent = relationship("FloatingIndent", back_populates="orders")

    # correct: one order → many junction rows
    order_items = relationship(
        "OrderJunction",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    short_close_items: Mapped[list["ShortCloseOrder"]] = relationship(
    "ShortCloseOrder",
    back_populates="order",
    cascade="all, delete-orphan"
    )

    billings: Mapped[list["Billing"]] = relationship(
    "Billing",
    back_populates="order",
    cascade="all, delete-orphan"
)



class OrderJunction(Base):
    __tablename__ = "order_junction"

    # =============== PRIMARY KEYS (COMPOSITE) ===============
    order_no: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.order_no"), primary_key=True
    )
    ledger_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ledger.ledger_id"), primary_key=True
    )
    vendor_code: Mapped[int] = mapped_column(
        Integer
    )
    vendor_id: Mapped[int] = mapped_column(
        Integer
    )
    cost:Mapped[Float] = mapped_column(Float)
    # =============== ITEM DETAILS ===============
    srl: Mapped[int | None] = mapped_column(Integer)
    part_no: Mapped[str | None] = mapped_column(String(50))
    nomenclature: Mapped[str | None] = mapped_column(String(200))

    au: Mapped[str | None] = mapped_column(String(10))
    qty_req: Mapped[int | None] = mapped_column(Integer)

    # =============== PRICE COLUMNS ===============
    psc: Mapped[Float | None] = mapped_column(Float)       # PSC price
    sme: Mapped[Float | None] = mapped_column(Float)       # SME price
    shlp: Mapped[Float | None] = mapped_column(Float)      # SHLP price
    shre: Mapped[Float | None] = mapped_column(Float)      # SHRE price
    sps: Mapped[Float | None] = mapped_column(Float)       # SPS price

    firm_quote: Mapped[str | None] = mapped_column(String(50))

    lowest_rate: Mapped[Float | None] = mapped_column(Float)
    gst: Mapped[Float | None] = mapped_column(Float)
    amount: Mapped[Float | None] = mapped_column(Float)

    pnc: Mapped[Float | None] = mapped_column(Float)
    pnc_with_tax: Mapped[Float | None] = mapped_column(Float)
    negotiable_amount: Mapped[Float | None] = mapped_column(Float)

    # =============== LPR DETAILS ===============
    lpr_no: Mapped[str | None] = mapped_column(String(10))
    lpr_date: Mapped[Date | None] = mapped_column(Date)

    # =============== JOB DETAILS ===============
    job_no: Mapped[str | None] = mapped_column(String(6))
    job_date: Mapped[Date | None] = mapped_column(Date)
    job_comp_type: Mapped[str | None] = mapped_column(String(10))

    # =============== RELATIONSHIPS ===============
    order: Mapped["Orders"] = relationship(
    "Orders",
    back_populates="order_items"
    )

    ledger: Mapped["Ledger"] = relationship(
        "Ledger",
        back_populates="ledger_order_items"
    )

class ShortCloseOrder(Base):
    __tablename__ = "short_close_order"

    # ---- PRIMARY KEY ----
    s_co_no: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # ---- FOREIGN KEYS ----
    order_no: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_no"),
        nullable=False
    )

    vendor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vendor_master.vendor_id"),
        nullable=False
    )

    # ---- EXTRA FIELDS ----
    order_date: Mapped[Date | None] = mapped_column(Date)
    received_rate: Mapped[float | None] = mapped_column(Float)
    order_rate: Mapped[float | None] = mapped_column(Float)

    # ---- RELATIONSHIPS ----
    order: Mapped["Orders"] = relationship(
        "Orders",
        back_populates="short_close_items"
    )

    vendor: Mapped["VendorMaster"] = relationship(
        "VendorMaster",
        back_populates="short_close_orders"
    )

