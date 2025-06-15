from fastapi import APIRouter, Request, Query
from typing import Optional
from starlette import status

from modules.exceptions import ExceptionMessages, RequestError
from modules.logger import logger
from modules.dependencies import session_depend, auth_depend, wallet_manager_depend

from .manager import WalletManager
from .schemas import WalletResponse

router = APIRouter(
    tags=["v1/wallets"],
)


@router.get(
    path="/{wallet_uuid}/",
    response_model=WalletResponse,
    summary="Get wallet by id",
    status_code=status.HTTP_200_OK,
)
async def get_wallet(
    session: session_depend,
    user: auth_depend,
    manager: wallet_manager_depend,
    wallet_uuid: int
) -> WalletResponse:
    """
    Retrieve wallet by id.
    """
    return await manager.get_wallet_by_id(session=session, user=user, id=wallet_uuid)


@router.post(
    path="/{wallet_uuid}/operation",
    response_model=WalletResponse,
    summary="Wallet operations",
    status_code=status.HTTP_201_CREATED,
)
async def wallet_operation(
    session: session_depend,
    user: auth_depend,
    manager: wallet_manager_depend,
    request_data: PostWalletOperation,
) -> TaskResponse:
    """
    Create task.

    """
    new_task_id = await manager.create_task(
        session=session, user=user, request_data=request_data
    )
    task = await manager.get_task_by_id(
        session=session, user=user, id=new_task_id, include_deleted_documents=False
    )

    return TaskResponseWorkflow(task=task, workflow_schema=manager.workflow.task)

@router.delete(
    path="/task/{task_id}",
    summary="Delete task by id",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="No Content",
)
async def delete_task_by_id(
    session: session_depend,
    user: auth_depend,
    manager: task_manager_depend,
    task_id: int,
) -> None:
    """
    Delete task by id.
    """
    await manager.get_task_by_id(
        session=session, user=user, id=task_id, include_deleted_documents=True
    )

    if manager.task.state.name != "draft":
        error = ExceptionMessages.DELETE_TASK_EXCEPTION.value
        message = "Невозможно удалить задачу вне статуса Черновик"
        logger.error(f"{error}: {message}")
        raise RequestError(error=error, message=message)
    await manager.delete_task(session=session, user=user)
