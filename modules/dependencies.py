import jwt
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker
from schemas.app import UserSchema

http_bearer = HTTPBearer()
token_depend = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]

async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_auth_user(credentials: token_depend) -> UserSchema | None:
    token = credentials.credentials
    token_payload = jwt.decode(token, options={"verify_signature": False})
    return UserSchema(**token_payload)

session_depend = Annotated[AsyncSession, Depends(get_db_async)]
auth_depend = Annotated[UserSchema, Depends(get_auth_user)]