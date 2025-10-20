# app/models/payment.py
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Payment(Base):
    __tablename__ = "payments"

    payment_uuid = Column(String, primary_key=True, default=generate_uuid, index=True)
    account_uuid = Column(String, ForeignKey("accounts.account_uuid"))
    amount = Column(Float)
    description = Column(String)

    # Relación con Account
    account = relationship("Account", back_populates="payments")
