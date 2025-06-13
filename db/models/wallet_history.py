import datetime

import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import SQLAlchemyBase

class WalletHistoryORM(SQLAlchemyBase):
    __tablename__ = "wallet_history"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(sa.ForeignKey("task.id"), nullable=False)
    action: Mapped[str] = sa.Column(sa.String, nullable=False)
    action_author: Mapped[str] = sa.Column(sa.String, nullable=False)
    modified_at: Mapped[datetime.datetime] = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.now
    )
    comment: Mapped[str] = sa.Column(sa.String, nullable=True)
    
    wallet: Mapped["WalletORM"] = relationship(
        back_populates="wallet_history",
        foreign_keys=[wallet_id],
        lazy="selectin"
    )