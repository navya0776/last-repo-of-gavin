from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .depot_demand import Demand


class MasterTable(Base):
    __tablename__ = "master_table"

    Ledger_code: Mapped[str] = mapped_column(String(4), primary_key=True,
                                             nullable=False)
    eqpt_code: Mapped[str] = mapped_column(String(4),
                                           unique=True,
                                           nullable=False)
    ledger_name: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=False)

    Ledger_code: Mapped[str] = mapped_column(
        String(4),
        primary_key=True,
        nullable=False
    )

    head: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    dmd: Mapped[list["Demand"]] = relationship(
        "Demand",
        back_populates="eqpt",
        cascade="all, delete",
        foreign_keys=[Demand.eqpt_code]
    )

    cds_Eqpt: Mapped["CDS"] = relationship("CDS", back_populates="Eqpt_cds")

    legder: Mapped["Ledger"] = relationship(
        "Ledger",
        back_populates="Eqpt",
        cascade="all, delete"
    )

    job: Mapped[list["JobMaster"]] = relationship(
        "JobMaster",
        back_populates="Eqpt",
        cascade="all, delete"
    )
