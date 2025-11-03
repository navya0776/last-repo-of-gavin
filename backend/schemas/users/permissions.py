from pydantic import BaseModel, model_validator


class BasePermissions(BaseModel):
    read: bool
    write: bool

    @model_validator(mode="after")
    def check_permissions(self):
        """
        Ensures:
        If 'write' is True, then 'read' must also be True.
        """
        if self.write and not self.read:
            self.read = True
        return self


class Permissions(BaseModel):
    ledger: BasePermissions
    apd: BasePermissions
    overhaul_scale: BasePermissions
    recieve_voucher: BasePermissions
    issue_voucher: BasePermissions

    local_purchase_indent: BasePermissions
    local_purchase_quotation: BasePermissions
    local_purchase_recieved: BasePermissions
    local_purchase_ordinance: BasePermissions
    local_purchase_pay: BasePermissions
    local_purchase_query: BasePermissions
    local_purchase_ammend: BasePermissions
