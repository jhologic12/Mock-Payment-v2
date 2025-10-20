from pydantic import BaseModel
from typing import List
import uuid

class PaymentBase(BaseModel):
    status: str
    remaining_balance: float

class PaymentCreate(PaymentBase):
    account_id: uuid.UUID

class PaymentItem(BaseModel):
    payment_id: uuid.UUID
    status: str
    remaining_balance: float

class PaymentResponse(BaseModel):
    account_id: uuid.UUID
    payments: List[PaymentItem]

    class Config:
        orm_mode = True
