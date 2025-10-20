# app/models/card.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Card(Base):
    __tablename__ = "cards"

    card_uuid = Column(String, primary_key=True, default=generate_uuid, index=True)
    account_uuid = Column(String, ForeignKey("accounts.account_uuid"))
    card_number = Column(String, unique=True, index=True)
    holder_name = Column(String)
    expiration_date = Column(String)
    cvv = Column(String)

    # Relación con Account
    account = relationship("Account", back_populates="cards")
