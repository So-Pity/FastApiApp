import datetime

import sqlalchemy as sa
from typing import List
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import SQLAlchemyBase
from .wallet_history import WalletHistoryORM

class WalletORM(SQLAlchemyBase):
    __tablename__ = "wallet"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    owner_id: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.now
    )
    amount: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    comment: Mapped[str] = sa.Column(sa.String, nullable=True)
    is_active: Mapped[bool] = sa.Column(sa.Boolean, nullable=False,default=True)
    
    wallet_history: Mapped[List["WalletHistoryORM"]] = relationship(
        "WalletHistoryORM",
        back_populates="wallet",
        lazy="selectin",
        order_by="WalletHistoryORM.id"
    )
