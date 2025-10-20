# app/schemas/payment_schema.py
from pydantic import BaseModel
from uuid import UUID

class PaymentCreate(BaseModel):
    account_uuid: UUID
    amount: float
    description: str

class PaymentResponse(BaseModel):
    payment_uuid: UUID
    account_uuid: UUID
    amount: float
    description: str
    status: str  # aprobado o rechazado

    class Config:
        orm_mode = True
