from datetime import datetime, date
from pydantic import BaseModel

class UserSchema(BaseModel):
    userName: str
    email: str
    fullName: str 
    createdAt: date
    lastLoginAt: datetime
    address: str
