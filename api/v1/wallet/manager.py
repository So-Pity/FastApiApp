from modules.logger import logger
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.app import UserSchema
from modules.exceptions import NotFoundError, RequestError, ExceptionMessages
from db.models import WalletORM, WalletHistoryORM
from db.operations import wallet_db, wallet_history_db
from .schemas import WalletResponse


class WalletManager:
    """Class for performing operations with wallets."""

    def __init__(self) -> None:
        self.wallet = None

    async def get_wallet_by_id(
        self,
        session: AsyncSession,
        user: UserSchema,
        id: int,
    ) -> WalletORM:
        """Retrieve wallet by wallet id.

        Args:
            id: Wallet id.

        Returns:
            Response containing wallet info.

        """
        try:
            self.wallet: WalletORM = await wallet_db.get_instance(session=session, id=id)
            if not self.wallet:
                logger.error(f"{ExceptionMessages.GET_WALLET_BY_ID_EXCEPTION.value}")
                raise NotFoundError(
                    error=ExceptionMessages.GET_WALLET_BY_ID_EXCEPTION.value,
                    message="Wallet not found",
                )

            return self.wallet
        except Exception as e:
            logger.error(
                f"{ExceptionMessages.GET_WALLET_ERROR.value} details: {e}"
            )  # exc_info=True
            raise RequestError(
                error=ExceptionMessages.GET_WALLET_ERROR.value,
                message="Error during getting wallet",
            )

    async def delete_wallet(self, session: AsyncSession, user: UserSchema) -> None:
        update_kwargs = {"is_active": False, "updated_at": datetime.now(timezone.utc)}

        try:
            await wallet_db.update_instance(
                session=session,
                where_attribute="id",
                where_value=self.wallet.id,
                update_kwargs=update_kwargs,
            )
            await session.flush()

            wallet_history_obj: WalletHistoryORM = await wallet_history_db.create_instance(
                session=session,
                wallet_id=self.wallet.id,
                action="Deletion",
                action_author=user.fullName,
            )
            await session.commit()

            self.wallet.wallet_history.append(wallet_history_obj)

            await session.refresh(self.wallet)
        except Exception as e:
            await session.rollback()
            logger.error(
                f"{ExceptionMessages.DELETE_WALLET_ERROR.value} details: {e}"
            )  # exc_info=True
            raise RequestError(
                error=ExceptionMessages.DELETE_WALLET_ERROR.value,
                message="Unable to delete wallet",
            )
