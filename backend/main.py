import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

from dotenv import load_dotenv
from fastapi import FastAPI

from data.database import init_mongo, init_redis

load_dotenv()

logger = getLogger(__name__)

DEBUG = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis, client = await asyncio.gather(init_redis(), init_mongo())

    yield

    await asyncio.gather(redis.close(), client.close())


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=DEBUG)
