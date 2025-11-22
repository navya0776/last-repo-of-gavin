from sqlalchemy import ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

# class CentralDemand(Base):
#     __tablename__ = "central_demand"

#     eqpt_code: Mapped[int] = mapped_column(Integer, primary_key=True)
#     Ledger_code: Mapped[int] = mapped_column(Integer, ForeignKey("ledgers.Ledger_code"))
#     nomen: Mapped[str] = mapped_column(String(50))
#     eqpt_name: Mapped[str] = mapped_column(String(50), unique=True)
#     head: Mapped[str] = mapped_column(String(20))
#     section: Mapped[str] = mapped_column(String(20))
#     jobs: Mapped[list["Job"]] = relationship("Job", back_populates="cds_dmd")


# ===========================
# Job Master
# ===========================
class JobMaster(Base):
    __tablename__ = "job_master"

    # ---- PRIMARY KEY ---- #
    job_no: Mapped[str] = mapped_column(String(6), primary_key=True)
    # --- FOREIGN KEY ---- #
    master_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("master_table.Master_id"), nullable=False)

    # ---- OTHER FIELDS ---- #
    eqpt_code: Mapped[str] = mapped_column(
        String(4), nullable=False)
    eqpt_name: Mapped[str] = mapped_column(String(50))
    job_date: Mapped[date] = mapped_column(Date)
    no_eqpt: Mapped[int] = mapped_column(Integer)
    no_comp: Mapped[int] = mapped_column(Integer, nullable=True)
    date_comp: Mapped[date] = mapped_column(Date, nullable=True)
    item_dem: Mapped[int] = mapped_column(Integer, nullable=True)
    full_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    part_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    nil_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    bal_itens: Mapped[int] = mapped_column(Integer)
    cancel_nr: Mapped[int] = mapped_column(Integer, nullable=True)
    on_LPR: Mapped[int] = mapped_column(Integer, nullable=True)
    enq_placed: Mapped[int] = mapped_column(Integer, nullable=True)
    SO_placed: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_full: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_part: Mapped[int] = mapped_column(Integer, nullable=True)
    cancel_prog: Mapped[int] = mapped_column(Integer, nullable=True)
    MT_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    ENGR_LP: Mapped[int] = mapped_column(Integer)
    ORD_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    TOTAL_LP: Mapped[int] = mapped_column(Integer)
    LP_access_date: Mapped[date] = mapped_column(Date)
    comit_type: Mapped[str] = mapped_column(String, nullable=True)
    VIR1: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_DT1: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_DEM1: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_ISS1: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR2: Mapped[int] = mapped_column(Integer, nullable=True)
    VIT_DT2: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_DEM2: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_ISS2: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR3: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_DT3: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_DEM3: Mapped[int] = mapped_column(Integer, nullable=True)
    VIR_ISS3: Mapped[int] = mapped_column(Integer, nullable=True)
    # ---- Add Job ----
    job_prefix: Mapped[str | None] = mapped_column(String(20))
    qty_on_job: Mapped[int | None] = mapped_column(Integer)
    job_suffix: Mapped[str | None] = mapped_column(String(20))
    depot: Mapped[str | None] = mapped_column(String(50))
    dep_wo: Mapped[str | None] = mapped_column(String(50))
    wo_date: Mapped[date | None] = mapped_column(Date)
    nature_rep: Mapped[str | None] = mapped_column(String(20))
    dt_received: Mapped[date | None] = mapped_column(Date)
    prod_started: Mapped[date | None] = mapped_column(Date)
    qty_completed: Mapped[int | None] = mapped_column(Integer)
    remarks: Mapped[str | None] = mapped_column(String(255))
    ahq_srl: Mapped[str | None] = mapped_column(String(50))
    make: Mapped[str | None] = mapped_column(String(50))
    model: Mapped[str | None] = mapped_column(String(50))
    ch_no: Mapped[str | None] = mapped_column(String(50))
    cum_tot: Mapped[int | None] = mapped_column(Integer)
    VIR_supp: Mapped[int | None] = mapped_column(Integer)
    ohs: Mapped[str | None] = mapped_column(String(50))
    date_completed: Mapped[date | None] = mapped_column(Date)
    catalogue_ref: Mapped[str | None] = mapped_column(String(50))
    em_ba_no_eng: Mapped[str | None] = mapped_column(String(50))
    tgt_date: Mapped[date | None] = mapped_column(Date)
    unit: Mapped[str | None] = mapped_column(String(10))
    eng_no: Mapped[str | None] = mapped_column(String(20))
    eng_job: Mapped[str | None] = mapped_column(String(20))
    eng_job_date: Mapped[date | None] = mapped_column(Date)
    sub_assy_job: Mapped[str | None] = mapped_column(String(20))
    sub_assy_date: Mapped[date | None] = mapped_column(Date)
    bd_srl: Mapped[str | None] = mapped_column(String(20))
    prog: Mapped[float | None] = mapped_column(Float)
    gang_ldr: Mapped[str | None] = mapped_column(String(50))

    # ---- Relationships ----
    Eqpt: Mapped["MasterTable"] = relationship(
        "MasterTable", back_populates="job")
    jobs: Mapped[list["CDS"]] = relationship("CDS", back_populates="demands")
    job_lpr: Mapped["LPR"] = relationship("LPR", back_populates="lpr_job")

    # Many-to-many relationship to Ledger via association table `job_ledger`
    ledgers: Mapped[list["Ledger"]] = relationship(
        "Ledger",
        secondary="job_ledger",
        back_populates="jobs",
        lazy="select",
    )


# ===========================
# CDS Table
# ===========================


class CDS(Base):
    __tablename__ = "cds"
    # ---- PRIMARY KEY ---- #
    dem_id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                        autoincrement=True)
    # ---- FOREIGN KEYS ---- #
    job_no: Mapped[str] = mapped_column(String(6), ForeignKey("job_master.job_no"
                                                              ))
    master_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("master_table.Master_id"
                                                      ))
    dem_no: Mapped[int] = mapped_column(Integer, nullable=False)

    eqpt_code: Mapped[str] = mapped_column(String(4), nullable=False)

    job_date: Mapped[date] = mapped_column(Date, nullable=False)
    dem_date: Mapped[date | None] = mapped_column(Date)

    demands: Mapped["JobMaster"] = relationship("JobMaster", back_populates="jobs")
    Eqpt_cds: Mapped["MasterTable"] = relationship(
        "MasterTable", back_populates="cds_Eqpt")

    cds_cdsJunc: Mapped["CdsJunction"] = relationship("CdsJunction",
                                                      back_populates="cdsJunc_cds")


# ===========================
# JUNCTION TABLE
# ===========================


class CdsJunction(Base):
    __tablename__ = "cds_junction"
    ledger_page_id: Mapped[int] = mapped_column(Integer,
                                            primary_key=True)
    demand_no: Mapped[int] = mapped_column(Integer, ForeignKey("cds.dem_id"))
    ledger_page: Mapped[str] = mapped_column(String(20),
                                             ForeignKey("ledger.ledger_page"),
                                             )
    ohs_no: Mapped[int] = mapped_column(Integer, nullable=True)
    part_number: Mapped[str] = mapped_column(String(50), nullable=True)
    spart_no: Mapped[str] = mapped_column(String(50), nullable=True)
    nomenclature: Mapped[str] = mapped_column(String(100), nullable=True)
    auth_officer: Mapped[str] = mapped_column(String(50), nullable=True)
    dem_ref_no: Mapped[int] = mapped_column(Integer, nullable=True)
    add_dem_no: Mapped[int] = mapped_column(Integer, nullable=True)
    lpr_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    lpr_no: Mapped[str] = mapped_column(String(20), nullable=True)
    lpr_date: Mapped[date] = mapped_column(Date, nullable=True)
    demand_ctrl_no: Mapped[str] = mapped_column(String(20), nullable=True)
    demand_ctrl_date: Mapped[date] = mapped_column(Date, nullable=True)
    curr_stock: Mapped[int] = mapped_column(Integer, nullable=True)
    now_issue_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_qty: Mapped[int] = mapped_column(Integer, nullable=True)
    date_nr: Mapped[date] = mapped_column(Date, nullable=True)
    oss_qty1: Mapped[int] = mapped_column(Integer, nullable=True)
    oss_iv1: Mapped[str] = mapped_column(String(20), nullable=True)
    oss_ivdt1: Mapped[date] = mapped_column(Date, nullable=True)
    oss_qty2: Mapped[int] = mapped_column(Integer, nullable=True)
    oss_iv2: Mapped[str] = mapped_column(String(20), nullable=True)
    oss_ivdt2: Mapped[date] = mapped_column(Date, nullable=True)
    oss_qty3: Mapped[int] = mapped_column(Integer, nullable=True)
    oss_iv3: Mapped[str] = mapped_column(String(20), nullable=True)
    oss_ivdt3: Mapped[date] = mapped_column(Date, nullable=True)
    cds_iv1: Mapped[str] = mapped_column(String(20), nullable=True)
    cds_ivdt1: Mapped[date] = mapped_column(Date, nullable=True)
    cds_qty2: Mapped[int] = mapped_column(Integer, nullable=True)
    cds_iv2: Mapped[str] = mapped_column(String(20), nullable=True)
    cds_ivdt2: Mapped[date] = mapped_column(Date, nullable=True)

    # ---- RELATIONSHIPS ---- #
    cdsJunc_cds:  Mapped["CDS"] = relationship(
        "CDS", back_populates="cds_cdsJunc")
    ledger_cds: Mapped["Ledger"] = relationship(
        "Ledger", back_populates="cds_ledger")


# ===========================
# CDS table
# ===========================


class cds_table(Base):
    __tablename__ = "cds_table"

    # ---- PRIMARY KEY ---- #
    cds_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # ---- FOREIGN KEYS ---- #
    Master_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("master_table.Master_id"),
        nullable=False
    )

    # ---- OTHER FIELDS ----

    equipment_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    ledger_code: Mapped[str] = mapped_column(
        String(4),
        nullable=False
    )

    eqpt_code: Mapped[str] = mapped_column(
        String(4),
        nullable=False
    )

    grp: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    head: Mapped[str] = mapped_column(String(15), nullable=False)

    # ---- RELATIONSHIPS ----
    eqpt: Mapped["MasterTable"] = relationship(
        "MasterTable",
        back_populates="added_eqpt", foreign_keys=[Master_id])
