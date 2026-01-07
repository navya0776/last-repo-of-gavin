import string
import asyncio
from hashlib import sha256
from secrets import choice

from sqlalchemy import insert
from data.models.lock import Lock
from data.database.database import AsyncSessionLocal as async_session_maker


def generate_password(length=13):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(choice(alphabet) for _ in range(length))
    return password, sha256(password.encode()).hexdigest()


async def insert_one(is_purchase_key=False):
    plain, hashed = generate_password()

    async with async_session_maker() as session:
        await session.execute(
            insert(Lock).values(key=hashed, is_purchase_key=is_purchase_key)
        )
        await session.commit()

    return plain  # Return plaintext so you can save it


async def insert_passwords():
    tasks = []

    # 99 normal keys
    for _ in range(99):
        tasks.append(insert_one(False))

    # 1 purchase key
    tasks.append(insert_one(True))

    passwords = await asyncio.gather(*tasks)
    return passwords


async def main():
    passwords = await insert_passwords()

    print("Generated keys:")
    for p in passwords:
        print(p)


if __name__ == "__main__":
    asyncio.run(main())
