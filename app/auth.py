import os

from fastapi import HTTPException, Request


API_KEY = os.environ.get("API_KEY") or None


async def check_api_key(request: Request) -> None:
    if API_KEY is None:
        return
    provided = request.headers.get("Apikey")
    if provided != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
