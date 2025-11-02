from fastapi import APIRouter, Depends

from backend.schemas.ledger import StoreWithLedgers
from backend.schemas.users import User

from backend.services.ledger import AllStores
from backend.core.middleware import get_current_user

router = APIRouter()


@router.get("/")
async def get_all_ledgers_with_stores(user: dict[str, str] = Depends(get_current_user)):
    username = user["user_id"]
