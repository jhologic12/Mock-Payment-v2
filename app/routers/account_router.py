# app/routers/account_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.services.account_service import create_account, get_account_by_uuid
from app.database import get_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountResponse)
def create_account_endpoint(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, account)

@router.get("/{account_uuid}", response_model=AccountResponse)
def get_account(account_uuid: str, db: Session = Depends(get_db)):
    db_account = get_account_by_uuid(db, account_uuid)
    if not db_account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return db_account
