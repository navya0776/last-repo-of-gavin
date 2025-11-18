from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .depot_demand import Demand
from .cds import cds_table
from .ledgers import Ledger

class MasterTable(Base):
    __tablename__ = "master_table"

    Ledger_code: Mapped[str] = mapped_column(String(4), primary_key=True,
                                             nullable=False)
    eqpt_code: Mapped[str] = mapped_column(String(4),
                                           unique=True,
                                           nullable=False)
    ledger_name: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=False)

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
        cascade="all, delete", foreign_keys=[Ledger.Ledger_code]
    )

    job: Mapped[list["JobMaster"]] = relationship(
        "JobMaster",
        back_populates="Eqpt",
        cascade="all, delete"
    )
    
    added_eqpt: Mapped["cds_table"] = relationship(
        "cds_table", back_populates="", cascade="all, delete", foreign_keys=[cds_table.eqpt_code])