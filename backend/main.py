import asyncio
from fastapi import FastAPI

from contextlib import asynccontextmanager
from logging import getLogger
from dotenv import load_dotenv

from data.database import init_redis, MongoManager

load_dotenv()

logger = getLogger(__name__)

DEBUG = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis, client = await asyncio.gather(init_redis(), MongoManager().init_client())

    yield

    await redis.close()
    client.close()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=DEBUG)
