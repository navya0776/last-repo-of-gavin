from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .depot_demand import Demand
from .cds import cds_table, JobMaster, CDS
from .ledgers import Ledger


class MasterTable(Base):
    __tablename__ = "master_table"

    Master_id: Mapped[int] = mapped_column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )

    Ledger_code: Mapped[str] = mapped_column(
        String(4), primary_key=True, nullable=False
    )

    eqpt_code: Mapped[str] = mapped_column(String(4), nullable=False)
    ledger_name: Mapped[str] = mapped_column(String(11), nullable=False)

    eqpt_name: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    dmd: Mapped[list["Demand"]] = relationship(
        "Demand",
        back_populates="eqpt",
        cascade="all, delete",
        foreign_keys=[Demand.master_id]
    )

    cds_Eqpt: Mapped["CDS"] = relationship("CDS", back_populates="Eqpt_cds")

    legder: Mapped["Ledger"] = relationship(
        "Ledger",
        back_populates="Eqpt",
        cascade="all, delete",
        foreign_keys=[Ledger.Master_id],
    )

    job: Mapped[list["JobMaster"]] = relationship(
        "JobMaster", back_populates="Eqpt", cascade="all, delete"
    )

    added_eqpt: Mapped["cds_table"] = relationship(
        "cds_table",
        back_populates="",
        cascade="all, delete",
        foreign_keys=[cds_table.Master_id],
    )
