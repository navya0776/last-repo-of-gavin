# This is Ducky
#      _
#  >(' )__
#    (  ._>
#     `--'
# Every time Mr. Puak doesn't pay us, Ducky commits 1 felony


import asyncio
from datetime import timedelta, timezone, datetime, MAXYEAR
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from hashlib import sha256

from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.lock import LockRequest, LockDetailsModel

from data.models import Lock, LockDetails
from data.database import get_db

router = APIRouter()

# Since timezone is default to UTC, and we need IST (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))


@router.post("/")
async def check_lock_key(request: LockRequest, session: AsyncSession = Depends(get_db)):
    hashed_key = sha256(request.key.encode()).hexdigest()

    is_purchase_key = await session.scalar(
        select(Lock.is_purchase_key).where(Lock.key == hashed_key)
    )

    if is_purchase_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid License Key!"
        )

    if is_purchase_key:
        # Ducky has been poid, Ducky is now happy as he can feed his family
        await session.execute(
            update(LockDetails)
            .where(LockDetails.id == 1)
            .values(
                recieved_payment=True,
                date=(
                    datetime(MAXYEAR, 12, 31, tzinfo=IST).replace(microsecond=0)
                ),  # This is roughly equivalent to year 9999, hopefully we get a contract by then
            )
        )

        return JSONResponse(
            status_code=200,
            content={"status": "purchase_key_valid", "expires": "9999-12-31"},
        )

    new_date = (datetime.now(IST) + timedelta(days=30)).replace(microsecond=0)

    await asyncio.gather(
        session.execute(
            update(LockDetails).where(LockDetails.id == 1).values(date=new_date)
        ),
        session.execute(delete(Lock).where(Lock.key == hashed_key)),
    )

    return JSONResponse(
        status_code=200,
        content={"status": "valid", "expires": new_date.isoformat()},
    )


@router.get("/")
async def have_we_been_payed_yet(session: AsyncSession = Depends(get_db)):
    data = await session.scalar(select(LockDetails).where(LockDetails.id == 1))

    # This is the first time the program is being loaded onto the server
    if data is None:
        await session.execute(
            insert(LockDetails).values(
                date=(datetime.now(IST) + timedelta(days=60)).replace(microsecond=0),
                recieved_payment=False,  # Assuming we don't get payed the second we deploy, Ducky will now start commiting felonies
            )
        )
        data = await session.scalar(select(LockDetails).where(LockDetails.id == 1))

    lock_data = LockDetailsModel.model_validate(data, from_attributes=True)

    if lock_data.recieved_payment:
        # YIPEEEEEEEEEEE MONEYY, DUCKY CAN FINALLY FEED HIS FAMILY
        return JSONResponse(
            status_code=200,
            content={
                "status": "paid",
                "expires": lock_data.date.isoformat(),
            },
        )

    # We have not been payed yet, Ducky has now commited a felony
    # Check if License key has expired or not
    now = datetime.now(IST).replace(microsecond=0)
    expiry = lock_data.date.astimezone(IST).replace(microsecond=0)

    if expiry >= now:
        return JSONResponse(
            status_code=200,
            content={
                "status": "valid",
                "expires": expiry.isoformat(),
            },
        )

    return JSONResponse(
        status_code=200,
        content={"status": "expired", "expires": expiry.isoformat()},
    )
