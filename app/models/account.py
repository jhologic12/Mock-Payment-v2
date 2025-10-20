# app/models/account.py
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Account(Base):
    __tablename__ = "accounts"

    account_uuid = Column(String, primary_key=True, default=generate_uuid, index=True)
    account_number = Column(String, unique=True, index=True)
    account_type = Column(String)
    owner_name = Column(String)
    balance = Column(Float)

    # Relaciones
    payments = relationship("Payment", back_populates="account", cascade="all, delete-orphan")
    cards = relationship("Card", back_populates="account", cascade="all, delete-orphan")
