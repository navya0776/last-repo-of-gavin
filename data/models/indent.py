from sqlalchemy import Boolean, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

class FloatingIndent(Base):
    __tablename__ = "floating_indent"



    indent_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    lpr_id: Mapped[str] = mapped_column(Integer, ForeignKey("lpr.lpr_id"))

    indent_no: Mapped[int] = mapped_column(Integer,nullable=True)
    indent_date: Mapped[date | None] = mapped_column(Date,nullable=True)

    

    prev_indent: Mapped[int | None] = mapped_column(Integer,nullable=True)
    prev_indent_date: Mapped[date | None] = mapped_column(Date,nullable=True)
    job_no: Mapped[str | None] = mapped_column(String(6))
    job_comp_date: Mapped[date | None] = mapped_column(Date,nullable=True)
    ty: Mapped[str | None] = mapped_column(String(2),nullable=True)
    eqpt_code: Mapped[str | None] = mapped_column(String(4),nullable=True)
    ledger_code: Mapped[str | None] = mapped_column(String(10),nullable=True)
    ledger_page: Mapped[str | None] = mapped_column(String(20),nullable=True)
    ohs_no: Mapped[str | None] = mapped_column(String(20),nullable=True)

    part_no: Mapped[str | None] = mapped_column(String(50),nullable=True)
    nomenclature: Mapped[str | None] = mapped_column(String(200),nullable=True)
    au: Mapped[str | None] = mapped_column(String(10),nullable=True)

    qty: Mapped[int | None] = mapped_column(Integer)
    issue: Mapped[int | None] = mapped_column(Integer,nullable=True)
    nr: Mapped[int | None] = mapped_column(Integer,nullable=True)
    rate: Mapped[int | None] = mapped_column(Integer,nullable=True)

    prev_indents_text: Mapped[str | None] = mapped_column(String(200),nullable=True)
    nr_reason_group: Mapped[str | None] = mapped_column(String(100),nullable=True)
    grp: Mapped[str | None] = mapped_column(String(50),nullable=True)
    head: Mapped[str] = mapped_column(String(100), nullable=False)


    prev_vendor: Mapped[str | None] = mapped_column(String(100),nullable=True)
    curr_vendor: Mapped[str | None] = mapped_column(String(100),nullable=True)
   
    supply_order1: Mapped[str | None] = mapped_column(String(100),nullable=True)
    v_cost: Mapped[float | None] = mapped_column(Float,nullable=True)
    


    vend2_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend1_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend3_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend4_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend5_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend6_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend7_id: Mapped[int | None] = mapped_column(Integer,nullable =True)
    vend8_id: Mapped[int | None] = mapped_column(Integer,nullable =True)

    vend2: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend1: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend3: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend4: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend5: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend6: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend7: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend8: Mapped[str | None] = mapped_column(String(50),nullable =True)

    vend1_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend2_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend3_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend4_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend5_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend6_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend7_so: Mapped[str | None] = mapped_column(String(50),nullable =True)
    vend8_so: Mapped[str | None] = mapped_column(String(50),nullable =True)

    supply_order_generated: Mapped[bool] = mapped_column(Boolean, default=False)
   

    # relationship to LPR
    lpr: Mapped["LPR"] = relationship("LPR", back_populates="indent_items")

    # relationship to UpdateVendor
   
    orders: Mapped[list["Orders"]] = relationship(
    "Orders",
    back_populates="indent"
    )



class VendorMaster(Base):
    __tablename__ = "vendor_master"

    vendor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vendor_code: Mapped[int] = mapped_column(String(20), nullable=False)
    vendor_name: Mapped[str] = mapped_column(String(100), nullable=False)

   
    S_NAME: Mapped[str | None] = mapped_column(String(100), nullable=True)
   
    ADD: Mapped[str | None] = mapped_column(String(255), nullable=True)
    CITY: Mapped[str | None] = mapped_column(String(100), nullable=True)
    E_MAIL: Mapped[str | None] = mapped_column(String(150), nullable=True)
    ACT: Mapped[str | None] = mapped_column(String(10), nullable=True)
    ALL_REF: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ALL_REFDT: Mapped[Date | None] = mapped_column(Date, nullable=True)
    PH_O: Mapped[str | None] = mapped_column(String(20), nullable=True)
    PH_R: Mapped[str | None] = mapped_column(String(20), nullable=True)
    MOBILE1: Mapped[str | None] = mapped_column(String(20), nullable=True)
    MOBILE2: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ITEM1: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ITEM2: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
   

    short_close_orders: Mapped[list["ShortCloseOrder"]] = relationship(
    "ShortCloseOrder",
    back_populates="vendor"
    )



# class UpdateVendors(Base):
#     __tablename__ = "update_vendors"

#     indent_no: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey("floating_indent.indent_no"),
#         primary_key=True
#     )

#     vendor_code: Mapped[int] = mapped_column(
#         ForeignKey("vendor_master.vendor_code"),
#         nullable=True,primary_key=True
#     )

#     prev_vendor: Mapped[str | None] = mapped_column(String(100))
#     curr_vendor: Mapped[str | None] = mapped_column(String(100))
#     supply_order: Mapped[bool] = mapped_column(Boolean,default=False)
#     v_cost: Mapped[float | None] = mapped_column(Float)
#     indent_date: Mapped[date | None] = mapped_column(Date)

#     vend1_so: Mapped[str | None] = mapped_column(String(50))
#     vend2_so: Mapped[str | None] = mapped_column(String(50))
#     vend3_so: Mapped[str | None] = mapped_column(String(50))
#     vend4_so: Mapped[str | None] = mapped_column(String(50))
#     vend5_so: Mapped[str | None] = mapped_column(String(50))
#     vend6_so: Mapped[str | None] = mapped_column(String(50))
#     vend7_so: Mapped[str | None] = mapped_column(String(50))
#     vend8_so: Mapped[str | None] = mapped_column(String(50))

#     indent: Mapped["FloatingIndent"] = relationship(
#         "FloatingIndent",
#         back_populates="vendor_details"
#     )
    
#     vendor: Mapped["VendorMaster"] = relationship(
#     "VendorMaster",
#     back_populates="vendor_updates"
#     )
