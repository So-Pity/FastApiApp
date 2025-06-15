from db import models
from .base import Database

wallet_db = Database(model=models.WalletORM)
wallet_history_db = Database(model=models.WalletHistoryORM)