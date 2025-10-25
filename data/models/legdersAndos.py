from typing import List, Optional

from pydantic import BaseModel, Field

# NOTE: I have written some comments to explain the models to who ever reads them for the first time.
# baad mei u can simply delete all the comments.


class AllStores(BaseModel):
    # Collection for storing all stores and their specific data.
    store_id: str
    location: str
    authority: str
    # abhi pta nhi hai humei aur..but u can add more, when u go on site to understand how stores are stored.


class LedgerMaintenance(BaseModel):
    # Ledger model for each equiment in the ledger maintainence sheet.
    ledger_page: str
    ohs_number: int
    isg_number: int
    ssg_number: int
    part_number: int
    nomenclature: str
    a_u: str
    no_off: int
    scl_auth: int
    unsv_stock: int
    rep_stock: int
    serv_stock: int
    msc: str
    floor_msc: str | None = None
    ved: str
    in_house: bool
    dues_in: int
    consumption: int
    bin_number: str
    group: str
    cds_unsv_stock: int
    cds_rep_stock: int
    cds_serv_stock: int
    lpp: str


class StoreLedgerDocument(BaseModel):
    # collection model for each store. dynamically created when a new store is added.
    equipment: str
    equipment_code: int
    ledgers: list[LedgerMaintenance]


class AllEquipments(BaseModel):
    # collection model to store all equiments and in which store they are present.
    # this will make easy the tracking of equiments in other sections of the software.
    equipment: str
    equipment_code: str
    store_id: str


class AllParts(BaseModel):
    # collection model to store all parts, so that tracking of stock and demand eases out.
    part_number: int
    nomenclature: str
    total_stock: int
    used_in_equipments: list[AllEquipments]
    dues_in: int
    dues_out: int
    demanded: int
    # the last 3 keys are guessed abhi. Replace them properly when On-Site.
