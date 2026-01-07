import asyncio
from hashlib import sha256

from data.database import init_db, get_db
from data.models import User as UserModel
from backend.schemas.users import User
from backend.schemas.users.permissions import Permissions, BasePermissions


def prompt_bool(prompt: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    raw = input(f"{prompt} ({suffix}): ").strip().lower()

    if raw == "":
        return default
    return raw in {"y", "yes", "true", "1"}


def prompt_permission(name: str) -> BasePermissions:
    print(f"\n{name.upper()}")

    read = prompt_bool("  Read access?", default=True)
    write = prompt_bool("  Write access?", default=False)

    return BasePermissions(read=read, write=write)


async def main():
    await init_db()
    permission_fields = Permissions.model_fields.keys()

    username = input("Enter username: ")
    password = input("Enter your password(Minimum 4 characters): ")
    is_admin = (
        input("Is user an admin? (True/False, default False): ").strip().lower()
        == "true"
    )

    if is_admin:
        data = {
            field: BasePermissions(read=True, write=True) for field in permission_fields
        }
    else:
        data = {field: prompt_permission(field) for field in permission_fields}

    permissions = Permissions(**data)
    user = User(
        username=username,
        password=sha256(password.encode()).hexdigest(),
        new_user=True,
        role="admin" if is_admin else "clerk",
        permissions=permissions,
    )

    async for session in get_db():
        data = UserModel(**user.model_dump())
        session.add(data)

    print("User added successfully!")


if __name__ == "__main__":
    asyncio.run(main())