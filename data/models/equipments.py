from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .base import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    eqpt_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    ledger_code: Mapped[str | None] = mapped_column(String(50), nullable=True)

    equipment_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # reverse relationship to Demand
    demands = relationship(
        "Demand",
        back_populates="equipment",
        primaryjoin="Equipment.eqpt_code == foreign(Demand.eqpt_code)",
        viewonly=True,
    )
