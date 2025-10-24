from fastapi import APIRouter, Request

from schemas.authentication import LoginRequest

app = APIRouter()


@app.post("/login")
async def login(credentials: LoginRequest):
    pass
