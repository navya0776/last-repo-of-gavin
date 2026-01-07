from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class AccountCard(Base):
    __tablename__ = "account_card"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    scale: Mapped[str] = mapped_column(String(10), nullable=True)
    ns: Mapped[str] = mapped_column(String(10), nullable=True)
    page: Mapped[int] = mapped_column(Integer, nullable=True)

    pt_no: Mapped[str] = mapped_column(String(20), nullable=True)
    part_no: Mapped[str] = mapped_column(String(50), nullable=True)

    item: Mapped[str] = mapped_column(String(255), nullable=True)

    no_off: Mapped[int] = mapped_column(Integer, nullable=True)
    auth: Mapped[int] = mapped_column(Integer, nullable=True)

    cabin: Mapped[str] = mapped_column(String(20), nullable=True)
    bin: Mapped[str] = mapped_column(String(20), nullable=True)

    voucher_no: Mapped[str] = mapped_column(String(30), nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=True)

    type: Mapped[str] = mapped_column(String(20), nullable=True)
    firm: Mapped[str] = mapped_column(String(50), nullable=True)

    qty: Mapped[Float] = mapped_column(Float, nullable=True)

    challan_job_no: Mapped[str] = mapped_column(String(30), nullable=True)
    challan_job_date: Mapped[Date] = mapped_column(Date, nullable=True)

    unsv_stk: Mapped[str] = mapped_column(String(5), nullable=True)
    rep_stk: Mapped[str] = mapped_column(String(5), nullable=True)
    ser_stk: Mapped[str] = mapped_column(String(5), nullable=True)
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class AccountCard(Base):
    __tablename__ = "account_card"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    scale: Mapped[str] = mapped_column(String(10), nullable=True)
    ns: Mapped[str] = mapped_column(String(10), nullable=True)
    page: Mapped[int] = mapped_column(Integer, nullable=True)

    pt_no: Mapped[str] = mapped_column(String(20), nullable=True)
    part_no: Mapped[str] = mapped_column(String(50), nullable=True)

    item: Mapped[str] = mapped_column(String(255), nullable=True)

    no_off: Mapped[int] = mapped_column(Integer, nullable=True)
    auth: Mapped[int] = mapped_column(Integer, nullable=True)

    cabin: Mapped[str] = mapped_column(String(20), nullable=True)
    bin: Mapped[str] = mapped_column(String(20), nullable=True)

    voucher_no: Mapped[str] = mapped_column(String(30), nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=True)

    type: Mapped[str] = mapped_column(String(20), nullable=True)
    firm: Mapped[str] = mapped_column(String(50), nullable=True)

    qty: Mapped[Float] = mapped_column(Float, nullable=True)

    challan_job_no: Mapped[str] = mapped_column(String(30), nullable=True)
    challan_job_date: Mapped[Date] = mapped_column(Date, nullable=True)

    unsv_stk: Mapped[str] = mapped_column(String(5), nullable=True)
    rep_stk: Mapped[str] = mapped_column(String(5), nullable=True)
    ser_stk: Mapped[str] = mapped_column(String(5), nullable=True)