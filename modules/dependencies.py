import jwt
from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker
from schemas.app import UserSchema
from api.v1.wallet.manager import WalletManager

http_bearer = HTTPBearer()
token_depend = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]

async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        await session.execute(text("SET LOCAL TRANSACTION ISOLATION LEVEL REPEATABLE READ")) #Data Race evade
        yield session

async def get_wallet_manager(fastapi_request: Request) -> WalletManager:
    return WalletManager()

async def get_auth_user(credentials: token_depend) -> UserSchema | None:
    token = credentials.credentials
    token_payload = jwt.decode(token, options={"verify_signature": False})
    return UserSchema(**token_payload)

session_depend = Annotated[AsyncSession, Depends(get_db_async)]
auth_depend = Annotated[UserSchema, Depends(get_auth_user)]
wallet_manager_depend = Annotated[WalletManager, Depends(get_wallet_manager)]