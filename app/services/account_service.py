# app/services/account_service.py
from sqlalchemy.orm import Session
from app.models.account import Account
import uuid

def create_account(db: Session, account_data):
    account = Account(
        account_number=account_data.account_number,
        account_type=account_data.account_type,
        owner_name=account_data.owner_name,
        balance=account_data.balance
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account_by_uuid(db: Session, account_uuid: str):
    return db.query(Account).filter(Account.account_uuid == account_uuid).first()
