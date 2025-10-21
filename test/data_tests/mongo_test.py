"""
Async Mongo smoke test for CI/CD
Checks if MongoDB responds to a ping command.
Requires: motor
"""

import os
import sys
import asyncio
import motor.motor_asyncio

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://admin:admin@localhost:27017/ims?authSource=admin")

async def main():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=2000)
        await client.admin.command("ping")
        print("mongo ok")
        return 0
    except Exception as e:
        print("mongo failed:", e, file=sys.stderr)
        return 1
    finally:
        client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
