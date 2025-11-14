from enum import unique
from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Equipment(Base):

    __tablename__ = "eqpt"

    Ledger_code: Mapped[str] = mapped_column(String(4), primary_key=True,
                                             nullable=False)
    eqpt_code: Mapped[str] = mapped_column(String(4),
                                           unique=True,
                                           nullable=False)
    eqpt_name: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)

    legder: Mapped["Ledger"] = relationship("Ledger", back_populates="Eqpt",
                           cascade="all, delete")

    dmd: Mapped["Demand"] = relationship("Demand", back_populates="eqpt", cascade="all, delete")

    job: Mapped[list["JobMaster"]] = relationship("JobMaster", back_populates="Eqpt", cascade="all, delete")

