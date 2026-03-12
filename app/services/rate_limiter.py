from fastapi import HTTPException
from app.services.cache_service import r

MAX_REQUESTS = 50
WINDOW_SECONDS = 60


def check_rate_limit(client_id: str):

    key = f"rate:{client_id}"

    current = r.get(key)

    if current is None:
        r.setex(key, WINDOW_SECONDS, 1)
        return

    if int(current) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    r.incr(key)