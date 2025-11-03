from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from backend.core.middleware import get_current_user
from backend.schemas.users.permissions import Permissions
from data.database import DBSession
from data.models.users import User


async def get_permissions(
    user=Depends(get_current_user), session=DBSession
) -> Permissions:
    stml = select(User.permissions).where(User.username == user["username"])

    result = await session.scalar(stml)
    assert result is not None, "User not found but passed authentication!"

    return Permissions.model_validate(result)


UserPermissions = Annotated[Permissions, Depends(get_permissions)]
