from pydantic import BaseModel, model_validator


class BasePermissions(BaseModel):
    read: bool
    write: bool

    @model_validator(mode="after")
    def check_permissions(self):
        """
        Ensures:
        1. 'read' must always be True.
        2. If 'write' is True, then 'read' must also be True.
        """
        if not self.read:
            raise ValueError("'read' permission must always be True.")
        if self.write and not self.read:
            raise ValueError("If 'write' is True, 'read' must also be True.")
        return self


class Ledger(BasePermissions): ...


class AdvanceProvisionDemand(BasePermissions): ...


class OverhaulScale(BasePermissions): ...


class RecieveVoucher(BasePermissions): ...


class IssueVoucher(BasePermissions): ...


class LocalPurhcaseIndent(BasePermissions): ...


class LocalPurchaseQuotation(BasePermissions): ...


class LocalPurchaseOrdinance(BasePermissions): ...


class LocalPurchaseRecieved(BasePermissions): ...


class LocalPurchasePay(BasePermissions): ...


class LocalPurchaseAmmend(BasePermissions): ...


class LocalPurchaseQuery(BasePermissions): ...


class Permissions(BaseModel):
    ledger: Ledger
    apd: AdvanceProvisionDemand
    overhaul_scale: OverhaulScale
    recieve_voucher: RecieveVoucher
    issue_voucher: IssueVoucher

    local_purchase_indent: LocalPurhcaseIndent
    local_purchase_quotation: LocalPurchaseQuotation
    local_purchase_recieved: LocalPurchaseRecieved
    local_purchase_ordinance: LocalPurchaseOrdinance
    local_purchase_pay: LocalPurchasePay
    local_purchase_query: LocalPurchaseQuery
    local_purchase_ammend: LocalPurchaseAmmend
