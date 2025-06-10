import jwt
from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import async_session_maker
from schemas.app import UserSchema
from api.v1.task.manager import TaskManager
from api.v1.document.manager import DocumentManager

http_bearer = HTTPBearer()
token_depend = Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]

async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    yield session

async def get_auth_user(credentials: token_depend) -> UserSchema | None:
  token = credentials.credentials
  token_payload = jwt.decode(token, options={"verify_signature": False})
  return UserSchema(**token_payload)

async def get_task_manager(fastapi_request: Request) -> TaskManager:
  return TaskManager(
    workflow=fastapi_request.app.workflow,
    directory=fastapi_request.app.directory
  )

async def get_document_manager(fastapi_request: Request) -> DocumentManager:
  return DocumentManager(
    workflow=fastapi_request.app.workflow,
    directory=fastapi_request.app.directory
  )
  

session_depend = Annotated[AsyncSession, Depends(get_db_async)]
auth_depend = Annotated[UserSchema, Depends(get_auth_user)]
task_manager_depend = Annotated[TaskManager, Depends(get_task_manager)]
document_manager_depend = Annotated[DocumentManager, Depends(get_document_manager)]