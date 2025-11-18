from pydantic import BaseModel, field_validator
from typing import Optional



# ---------------------------------------------------
class IndentBase(BaseModel):
    prev_indent: Optional[int] = None
    job_no: Optional[int] = None
    job_comp_type: Optional[str] = None
    eqpt_code: Optional[str] = None
    ledger_code: Optional[str] = None
    ledger_page: Optional[str] = None
    ohs_no: Optional[str] = None

    part_no: Optional[str] = None
    nomenclature: Optional[str] = None
    au: Optional[str] = None

    qty: Optional[int] = None
    issue: Optional[int] = None
    nr: Optional[int] = None
    rate: Optional[int] = None

    prev_indents_text: Optional[str] = None
    nr_reason_group: Optional[str] = None



# ---------------------------------------------------
class IndentCreate(IndentBase):
    lpr_no: int  # required

    @field_validator(
        "job_comp_type",
        "eqpt_code",
        "ledger_code",
        "ledger_page",
        "ohs_no",
        "part_no",
        "nomenclature",
        "au",
        "prev_indents_text",
        "nr_reason_group",
        mode="before"
    )
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v



# No validators here, only correct fields
# ---------------------------------------------------
class IndentResponse(IndentBase):
    indent_no: int
    lpr_no: int

    class Config:
        from_attributes = True



# ---------------------------------------------------
class IndentViewResponse(BaseModel):
    indent_no: int
    lpr_no: int
    job_no: Optional[int] = None
    part_no: Optional[str] = None
    nomenclature: Optional[str] = None
    qty: Optional[int] = None

    class Config:
        from_attributes = True
