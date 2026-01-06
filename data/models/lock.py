from datetime import datetime
from sqlalchemy import Date, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column as Column

from .base import Base


class Lock(Base):
    __tablename__ = "lock"

    key: Mapped[str] = Column(
        String(256), primary_key=True, unique=True, index=True, nullable=False
    )
    is_purchase_key: Mapped[bool] = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Defines if we have been paid for the project or not, only one True value exists",
    )


class LockDetails(Base):
    __tablename__ = "lock_details"

    id: Mapped[int] = Column(
        Integer, primary_key=True, default=1
    )  # This ensures that only 1 entry is their in the DB
    date: Mapped[datetime] = Column(Date, unique=True, index=True, nullable=False)
    recieved_payment: Mapped[bool] = Column(Boolean, unique=True, nullable=False)
