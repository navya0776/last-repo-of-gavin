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
    job_id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                        autoincrement=True)
    # --- FOREIGN KEY ---- #
    master_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("master_table.Master_id"), nullable=False)

    # ---- OTHER FIELDS ---- #
    job_no: Mapped[str] = mapped_column(String(6),nullable=True)
    eqpt_code: Mapped[str] = mapped_column(
        String(4), nullable=True)
    eqpt_name: Mapped[str] = mapped_column(String(50),nullable=True)
    job_date: Mapped[date] = mapped_column(Date, nullable=True)
    no_eqpt: Mapped[int] = mapped_column(Integer,nullable=True)
    no_comp: Mapped[int] = mapped_column(Integer, nullable=True)
    date_comp: Mapped[date] = mapped_column(Date, nullable=True)
    item_dem: Mapped[int] = mapped_column(Integer, nullable=True)
    full_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    part_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    nil_iss: Mapped[int] = mapped_column(Integer, nullable=True)
    bal_itens: Mapped[int] = mapped_column(Integer, nullable=True)
    cancel_nr: Mapped[int] = mapped_column(Integer, nullable=True)
    on_LPR: Mapped[int] = mapped_column(Integer, nullable=True)
    enq_placed: Mapped[int] = mapped_column(Integer, nullable=True)
    SO_placed: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_full: Mapped[int] = mapped_column(Integer, nullable=True)
    recd_part: Mapped[int] = mapped_column(Integer, nullable=True)
    so_nr_cancel: Mapped[int] = mapped_column(Integer, nullable=True)
    MT_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    ENGR_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    ORD_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    TOTAL_LP: Mapped[int] = mapped_column(Integer, nullable=True)
    LP_access_date: Mapped[date] = mapped_column(Date, nullable=True)
    comit_type: Mapped[str] = mapped_column(String, nullable=True)

    # ---- Add Job ----
    job_prefix: Mapped[str | None] = mapped_column(String(20), nullable=True)
    job_suffix: Mapped[str | None] = mapped_column(String(20), nullable=True)
    depot: Mapped[str | None] = mapped_column(String(50), nullable=True)
    dep_wo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    dep_wodate: Mapped[date | None] = mapped_column(Date, nullable=True)
    dt_received: Mapped[date | None] = mapped_column(Date, nullable=True)
    prod_started: Mapped[date | None] = mapped_column(Date, nullable=True)
    qty_completed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ahq_srl: Mapped[str | None] = mapped_column(String(50), nullable=True)
    make: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ch_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cum_tot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    VIR_supp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ohs: Mapped[str | None] = mapped_column(String(50), nullable=True)
    date_completed: Mapped[date | None] = mapped_column(Date, nullable=True)
    catalogue_ref: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # em_ba_no_eng
    em_ba_no_eng_1: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_2: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_3: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_4: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_5: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_6: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_7: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_8: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_9: Mapped[str | None] = mapped_column(String(50), nullable=True)
    em_ba_no_eng_10: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # table_date_completed
    table_date_completed_1: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_2: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_3: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_4: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_5: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_6: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_7: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_8: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_9: Mapped[date | None] = mapped_column(Date, nullable=True)
    table_date_completed_10: Mapped[date | None] = mapped_column(Date, nullable=True)

    # tgt_date
    tgt_date_1: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_2: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_3: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_4: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_5: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_6: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_7: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_8: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_9: Mapped[date | None] = mapped_column(Date, nullable=True)
    tgt_date_10: Mapped[date | None] = mapped_column(Date, nullable=True)

    # unit
    unit_1: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_2: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_3: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_4: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_5: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_6: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_7: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_8: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_9: Mapped[str | None] = mapped_column(String(10), nullable=True)
    unit_10: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # eng_no
    eng_no_1: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_2: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_3: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_4: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_5: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_6: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_7: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_8: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_9: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_no_10: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # eng_job
    eng_job_1: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_2: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_3: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_4: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_5: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_6: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_7: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_8: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_9: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eng_job_10: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # eng_job_date
    eng_job_date_1: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_2: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_3: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_4: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_5: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_6: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_7: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_8: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_9: Mapped[date | None] = mapped_column(Date, nullable=True)
    eng_job_date_10: Mapped[date | None] = mapped_column(Date, nullable=True)

    # sub_assy_no
    sub_assy_no_1: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_2: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_3: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_4: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_5: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_6: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_7: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_8: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_9: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sub_assy_no_10: Mapped[str | None] = mapped_column(String(50), nullable=True)


    # sub_assy_job
    sub_assy_job_1: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_2: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_3: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_4: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_5: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_6: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_7: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_8: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_9: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sub_assy_job_10: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # sub_assy_date
    sub_assy_date_1: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_2: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_3: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_4: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_5: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_6: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_7: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_8: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_9: Mapped[date | None] = mapped_column(Date, nullable=True)
    sub_assy_date_10: Mapped[date | None] = mapped_column(Date, nullable=True)

    # bd_srl
    bd_srl_1: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_2: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_3: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_4: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_5: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_6: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_7: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_8: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_9: Mapped[str | None] = mapped_column(String(20), nullable=True)
    bd_srl_10: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # prog
    prog_1: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_2: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_3: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_4: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_5: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_6: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_7: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_8: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_9: Mapped[float | None] = mapped_column(Float, nullable=True)
    prog_10: Mapped[float | None] = mapped_column(Float, nullable=True)

    # gang_ldr
    gang_ldr_1: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_2: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_3: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_4: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_5: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_6: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_7: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_8: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_9: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gang_ldr_10: Mapped[str | None] = mapped_column(String(50), nullable=True)


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
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey("job_master.job_id"
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
    ledger_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey("ledger.ledger_id"),
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
