from pydantic import BaseModel


class RolePermissions(BaseModel):
    """
    Defines the specific permissions for a role.
    This structure ensures fine-grained control over user actions.
    """

    read: bool
    write: bool
    delete: bool


class Role(BaseModel):
    """
    Collection model for defining all available roles and their associated permissions.
    This will likely be a separate collection in your database (e.g., 'roles').
    """

    role_name: str
    permissions: RolePermissions


class BasePermissions(BaseModel):
    read: bool
    write: bool
    delete: bool
    update: bool


class Permissions(BaseModel):
    ledger: BasePermissions
    issue_voucher: BasePermissions


class User(BaseModel):
    """
    Collection model for storing all user accounts.
    This will likely be your 'users' collection.
    """

    username: str
    password: str
    new_user: bool
    role: str
    permissions: Permissions
