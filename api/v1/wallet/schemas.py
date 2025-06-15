from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, AliasPath
from enum import Enum as PyEnum
from datetime import datetime

class AbstractName(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class AbstractNameComment(AbstractName):
    comment: Optional[str] = None

class WalletHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action: str
    state: str
    actionAuthor: str = Field(None, validation_alias="action_author")
    modifiedAt: datetime = Field(None, validation_alias="modified_at")
    comment: Optional[str] = None

class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: int
    comment: Optional[str] = None

    walletHistory: List[WalletHistory]

class WalletOperationType(PyEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    

class PostWalletOperation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation_type: WalletOperationType
    amount: int
