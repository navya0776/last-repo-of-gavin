import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

from dotenv import load_dotenv
from fastapi import FastAPI

from backend.routers.admin import admin_router
from backend.routers.authentication.routes import app as auth_router
from backend.routers.ledger.routes import router as ledger_router
from backend.routers.cds import router as cds_router
from backend.routers.demand.routes import router as demand_router

from data.database import init_db, init_redis, close_db, close_redis

load_dotenv()

logger = getLogger(__name__)

DEBUG = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.gather(init_redis(), init_db())

    yield

    await asyncio.gather(close_db(), close_redis())


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")
app.include_router(ledger_router, prefix="/ledger")
app.include_router(cds_router, prefix="/cds")
app.include_router(demand_router, prefix="/demand")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=DEBUG)
