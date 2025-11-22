from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class LPR(Base):
    __tablename__ = "lpr"

    # ----- PRIMARY KEY -----
    lpr_no: Mapped[int] = mapped_column(Integer, primary_key=True)

    # ----- FOREIGN KEYS -----
    job_no: Mapped[str] = mapped_column(
        String(6), ForeignKey("job_master.job_no"))

    # # ----- FIELDS -----
    # srl: Mapped[int] = mapped_column(Integer, nullable=True)
    # scale: Mapped[str] = mapped_column(String(10), nullable=True)
    # part_no: Mapped[str] = mapped_column(String(50), nullable=True)
    # nomenclature: Mapped[str] = mapped_column(String(100), nullable=True)
    # au: Mapped[str] = mapped_column(String(10), nullable=True)
    # qty: Mapped[int] = mapped_column(Integer, nullable=True)

    # ----- RELATIONSHIPS -----
    lpr_job: Mapped["JobMaster"] = relationship(
        "JobMaster", back_populates="job_lpr")
    lpr_junctions: Mapped[list["LPR_Junction"]] = relationship(
        "LPR_Junction", back_populates="lpr", cascade="all, delete-orphan")
    indent_items: Mapped[list["Indent"]] = relationship(
        "Indent", back_populates="lpr")
