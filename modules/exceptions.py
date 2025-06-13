from typing import Any, Optional, Dict

from fastapi import status
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from pydantic import BaseModel
from enum import Enum

from .logger import logger

class ErrorSchema(BaseModel):
    status: int
    error: str
    message: str

async def http_exception_handler(request, exc):
    content = ErrorSchema(
        status=exc.status_code,
        error=f"WALLET-API: {exc.error if hasattr(exc, 'error') else exc.detail}",
        message=exc.message if hasattr(exc, 'message') else ''
    ).model_dump(mode='json')
    if content['message'] == '':
        logger.error(content)
    return JSONResponse(content, status_code=exc.status_code)

async def validation_exception_handler(request, exc: RequestValidationError):
    error = exc.errors()
    content = ErrorSchema(
        status=422,
        error=f"WALLET-API: VALIDATION_ERROR: {str(error[0]['loc'])}: {error[0]['msg']}",
        message=f"Ошибка валидации данных"
    ).model_dump(mode='json')
    logger.error(f"{str(error[0]['loc'])}: {error[0]['msg']}")
    return JSONResponse(content, status_code=422)

class RequestOK(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_200_OK, headers)

class MultiStatusOK(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_207_MULTI_STATUS, headers)

class RequestError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_400_BAD_REQUEST, headers)

class UnauthorizedError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_401_UNAUTHORIZED, headers)

class AuthError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_403_FORBIDDEN, headers)

class NotFoundError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_404_NOT_FOUND, headers)

class DeletedError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_410_GONE, headers)

class NotImplementedError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_501_NOT_IMPLEMENTED, headers)

class ValidationError(HTTPException):
    def __init__(
        self,
        error: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.error = error
        self.message = message
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, headers)

class ExceptionMessages(str, Enum):
    GET_EXCEPTION = "GET_WALLET_ERROR"