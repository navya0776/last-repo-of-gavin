from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Indent(Base):
    __tablename__ = "indent"

    # ----- PRIMARY KEY -----
    indent_no: Mapped[int] = mapped_column(Integer, primary_key=True)

    # ----- FOREIGN KEY -----
    lpr_no: Mapped[str] = mapped_column(String(10), ForeignKey("lpr.lpr_no"), nullable=False)

    # ----- OTHER FIELDS (NO FKs) -----
    prev_indent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    job_no: Mapped[str | None] = mapped_column(String(6), nullable=True)
    job_comp_type: Mapped[str | None] = mapped_column(String(5))
    eqpt_code: Mapped[str | None] = mapped_column(String(4))
    ledger_code: Mapped[str | None] = mapped_column(String(10))
    ledger_page: Mapped[str | None] = mapped_column(String(20))
    ohs_no: Mapped[str | None] = mapped_column(String(20))

    part_no: Mapped[str | None] = mapped_column(String(50))
    nomenclature: Mapped[str | None] = mapped_column(String(200))
    au: Mapped[str | None] = mapped_column(String(10))

    qty: Mapped[int | None] = mapped_column(Integer)
    issue: Mapped[int | None] = mapped_column(Integer)
    nr: Mapped[int | None] = mapped_column(Integer)
    rate: Mapped[int | None] = mapped_column(Integer)

    prev_indents_text: Mapped[str | None] = mapped_column(String(200))
    nr_reason_group: Mapped[str | None] = mapped_column(String(100))

    # ----- RELATIONSHIP -----
    lpr: Mapped["LPR"] = relationship("LPR", back_populates="indent_items")
