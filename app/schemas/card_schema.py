from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class CardInfo(BaseModel):
    card_uuid: UUID
    last4: str
    holder_name: str
    expiration_date: str

    class Config:
        orm_mode = True

class AccountInfo(BaseModel):
    account_uuid: UUID
    owner_name: str
    account_number: str
    cards: List[CardInfo] = []  # Todas las tarjetas asociadas

    class Config:
        orm_mode = True

class CardCreate(BaseModel):
    account_uuid: str
    card_number: str = Field(..., min_length=12, max_length=16)
    holder_name: str
    expiration_date: str
    cvv: str = Field(..., min_length=3, max_length=4)

class CardResponse(BaseModel):
    card_uuid: UUID
    account_uuid: UUID
    holder_name: str
    expiration_date: str
    last4: str
    account: AccountInfo  # Información completa de la cuenta


class CardValidationRequest(BaseModel):
    card_number: str = Field(..., min_length=12, max_length=19)
    holder_name: str
    expiration_date: str  # formato MM/YY
    cvv: str = Field(..., min_length=3, max_length=4)






    class Config:
        orm_mode = True
