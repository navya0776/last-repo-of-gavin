from fastapi import APIRouter, Depends

from backend.services.ledger import get_all_ledgers
from backend.repositories import UserCollection
from backend.core.middleware import get_current_user

from data.models.users import User

router = APIRouter()


@router.get("/")
async def get_all_ledger(users: UserCollection, user=Depends(get_current_user)):
    get_all_ledgers()
