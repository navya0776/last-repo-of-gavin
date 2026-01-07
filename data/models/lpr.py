from sqlalchemy import Integer, String, ForeignKey,Float,Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date


class LPR(Base):
    __tablename__ = "lpr"

    # ----- PRIMARY KEY -----
    lpr_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


    lpr_no: Mapped[str] = mapped_column(String(10),nullable=True)
    lpr_date: Mapped[date] = mapped_column(Date, nullable=True)
    job_date: Mapped[date] = mapped_column(Date, nullable=True)
    head: Mapped[str] = mapped_column(String(100), nullable=False)
    

    # ----- FOREIGN KEYS -----
    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_master.job_id"), nullable=False)

    # # ----- FIELDS -----
    # srl: Mapped[int] = mapped_column(Integer, nullable=True)
    # scale: Mapped[str] = mapped_column(String(10), nullable=True)
    # part_no: Mapped[str] = mapped_column(String(50), nullable=True)
    # nomenclature: Mapped[str] = mapped_column(String(100), nullable=True)
    # au: Mapped[str] = mapped_column(String(10), nullable=True)
    # qty: Mapped[int] = mapped_column(Integer, nullable=True)

    # ----- RELATIONSHIPS -----
    lpr_job: Mapped["JobMaster"] = relationship("JobMaster", back_populates="job_lpr")

    lpr_junctions: Mapped[list["LPR_Junction"]] = relationship("LPR_Junction", back_populates="lpr",cascade="all, delete-orphan")
    indent_items: Mapped[list["FloatingIndent"]] = relationship("FloatingIndent", back_populates="lpr")



class LprClosed(Base):
    __tablename__ = "lpr_closed"

    # Primary key (nullable=False by default)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


    ledger_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey("ledger.ledger_id"),
                                             nullable=True
                                             )

    L_CODE: Mapped[str] = mapped_column(String(20), nullable=True)
    L_PAGE: Mapped[str] = mapped_column(String(20), nullable=True)
    ENQ_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    ENQ_DT: Mapped[Date] = mapped_column(Date, nullable=True)
    SCL_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    PART_NO: Mapped[str] = mapped_column(String(50), nullable=True)
    NOMEN: Mapped[str] = mapped_column(String(255), nullable=True)
    A_U: Mapped[str] = mapped_column(String(10), nullable=True)
    QTY: Mapped[float] = mapped_column(Float, nullable=True)

    SUP1: Mapped[str] = mapped_column(String(100), nullable=True)
    SUP2: Mapped[str] = mapped_column(String(100), nullable=True)
    SUP3: Mapped[str] = mapped_column(String(100), nullable=True)
    SUP4: Mapped[str] = mapped_column(String(100), nullable=True)

    REJ1: Mapped[str] = mapped_column(String(100), nullable=True)
    REJ2: Mapped[str] = mapped_column(String(100), nullable=True)
    REJ3: Mapped[str] = mapped_column(String(100), nullable=True)
    REJ4: Mapped[str] = mapped_column(String(100), nullable=True)

    DEALER: Mapped[str] = mapped_column(String(100), nullable=True)

    RATEQ: Mapped[float] = mapped_column(Float, nullable=True)
    RATEL: Mapped[float] = mapped_column(Float, nullable=True)

    SO_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    SO_DT: Mapped[Date] = mapped_column(Date, nullable=True)

    YN: Mapped[str] = mapped_column(String(5), nullable=True)

    PENQ_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    PENQ_DT: Mapped[Date] = mapped_column(Date, nullable=True)

    PRI: Mapped[str] = mapped_column(String(20), nullable=True)
    PRI_DT: Mapped[Date] = mapped_column(Date, nullable=True)

    INDL: Mapped[str] = mapped_column(String(20), nullable=True)
    REM: Mapped[str] = mapped_column(String(255), nullable=True)
    RC: Mapped[str] = mapped_column(String(20), nullable=True)

    REPEAT: Mapped[str] = mapped_column(String(10), nullable=True)

    OPT1: Mapped[str] = mapped_column(String(50), nullable=True)
    OPT2: Mapped[str] = mapped_column(String(50), nullable=True)
    OPT3: Mapped[str] = mapped_column(String(50), nullable=True)

    JOB_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    JOB_DT: Mapped[Date] = mapped_column(Date, nullable=True)

    LPR_NO: Mapped[str] = mapped_column(String(30), nullable=True)
    LPR_DT: Mapped[Date] = mapped_column(Date, nullable=True)

    URGENT: Mapped[str] = mapped_column(String(10), nullable=True)
    RF: Mapped[str] = mapped_column(String(10), nullable=True)
    NR: Mapped[str] = mapped_column(String(10), nullable=True)

    REMARKS: Mapped[str] = mapped_column(String(255), nullable=True)

    STOCK: Mapped[float] = mapped_column(Float, nullable=True)
    P_STOCK: Mapped[float] = mapped_column(Float, nullable=True)
    REQT: Mapped[float] = mapped_column(Float, nullable=True)

    GSTL: Mapped[float] = mapped_column(Float, nullable=True)

    date_completed: Mapped[Date] = mapped_column(Date, nullable=True)
    head: Mapped[str] = mapped_column(String(100), nullable=False)

    # ----- RELATIONSHIPS -----
    lpr_closed_ledger: Mapped["Ledger"] = relationship(
        "Ledger", back_populates="ledger_lpr_closed")