# app/schemas/account_schema.py
from pydantic import BaseModel
from uuid import UUID

class AccountCreate(BaseModel):
    account_number: str
    account_type: str
    owner_name: str
    balance: float

class AccountResponse(BaseModel):
    account_uuid: UUID
    account_number: str
    account_type: str
    owner_name: str
    balance: float

    class Config:
        orm_mode = True
