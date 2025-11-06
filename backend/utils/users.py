from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.middleware import get_current_user
from backend.schemas.users.permissions import Permissions

from data.models.users import User
from data.database import get_db


async def get_permissions(
    user=Depends(get_current_user), session: AsyncSession = Depends(get_db)
) -> Permissions:
    stml = select(User.permissions).where(User.username == user["username"])

    result = await session.scalar(stml)
    assert result is not None, "User not found but passed authentication!"

    return Permissions.model_validate(result)


UserPermissions = Annotated[Permissions, Depends(get_permissions)]
