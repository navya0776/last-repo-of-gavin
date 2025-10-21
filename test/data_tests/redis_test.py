"""
Redis smoke test for CI/CD
Checks if Redis responds to ping.
Requires: redis
"""

import os
import sys
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def main():
    try:
        client = redis.from_url(REDIS_URL, decode_responses=True)
        pong = client.ping()
        if pong in (True, "PONG"):
            print("redis ok")
            return 0
        else:
            print("redis unexpected ping response:", pong, file=sys.stderr)
            return 1
    except Exception as e:
        print("redis failed:", e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
