from sqlalchemy import Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

class FloatingIndent(Base):
    __tablename__ = "floating_indent"

    indent_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    lpr_id: Mapped[str] = mapped_column(Integer, ForeignKey("lpr.lpr_id"))

    prev_indent: Mapped[int | None] = mapped_column(Integer)
    job_no: Mapped[str | None] = mapped_column(String(6))
    job_comp_type: Mapped[str | None] = mapped_column(String(5))
    eqpt_code: Mapped[str | None] = mapped_column(String(4))
    ledger_code: Mapped[str | None] = mapped_column(String(10))
    ledger_page: Mapped[str | None] = mapped_column(String(20))
    ohs_no: Mapped[str | None] = mapped_column(String(20))

    part_no: Mapped[str | None] = mapped_column(String(50))
    nomenclature: Mapped[str | None] = mapped_column(String(200))
    au: Mapped[str | None] = mapped_column(String(10))

    qty: Mapped[int | None] = mapped_column(Integer)
    issue: Mapped[int | None] = mapped_column(Integer)
    nr: Mapped[int | None] = mapped_column(Integer)
    rate: Mapped[int | None] = mapped_column(Integer)

    prev_indents_text: Mapped[str | None] = mapped_column(String(200))
    nr_reason_group: Mapped[str | None] = mapped_column(String(100))

    # relationship to LPR
    lpr: Mapped["LPR"] = relationship("LPR", back_populates="indent_items")

    # relationship to UpdateVendor
    vendor_details: Mapped["UpdateVendors"] = relationship(
        "UpdateVendors",
        back_populates="indent",
        uselist=False
    )
    orders: Mapped[list["Orders"]] = relationship(
    "Orders",
    back_populates="indent"
    )



class VendorMaster(Base):
    __tablename__ = "vendor_master"

    vendor_code: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    vendor_updates: Mapped[list["UpdateVendors"]] = relationship(
    "UpdateVendors",
    back_populates="vendor",
    foreign_keys="UpdateVendors.vendor_code"
    )

    short_close_orders: Mapped[list["ShortCloseOrder"]] = relationship(
    "ShortCloseOrder",
    back_populates="vendor"
    )



class UpdateVendors(Base):
    __tablename__ = "update_vendors"

    indent_no: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("floating_indent.indent_no"),
        primary_key=True
    )

    vendor_code: Mapped[int] = mapped_column(
        ForeignKey("vendor_master.vendor_code"),
        nullable=True,primary_key=True
    )

    prev_vendor: Mapped[str | None] = mapped_column(String(100))
    curr_vendor: Mapped[str | None] = mapped_column(String(100))
    supply_order: Mapped[str | None] = mapped_column(String(50))
    v_cost: Mapped[float | None] = mapped_column(Float)
    indent_date: Mapped[date | None] = mapped_column(Date)

    vend1_so: Mapped[str | None] = mapped_column(String(50))
    vend2_so: Mapped[str | None] = mapped_column(String(50))
    vend3_so: Mapped[str | None] = mapped_column(String(50))
    vend4_so: Mapped[str | None] = mapped_column(String(50))
    vend5_so: Mapped[str | None] = mapped_column(String(50))
    vend6_so: Mapped[str | None] = mapped_column(String(50))
    vend7_so: Mapped[str | None] = mapped_column(String(50))
    vend8_so: Mapped[str | None] = mapped_column(String(50))

    indent: Mapped["FloatingIndent"] = relationship(
        "FloatingIndent",
        back_populates="vendor_details"
    )
    
    vendor: Mapped["VendorMaster"] = relationship(
    "VendorMaster",
    back_populates="vendor_updates"
    )
