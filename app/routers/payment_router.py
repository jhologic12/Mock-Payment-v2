# app/routers/payment_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payment_schema import PaymentCreate, PaymentResponse
from app.services.payment_service import create_payment
from app.database import get_db
from app.models.card import Card

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment_endpoint(payment: PaymentCreate, db: Session = Depends(get_db)):
    result = create_payment(db, payment)
    if result["status"] == "rechazado":
        raise HTTPException(status_code=400, detail=result["message"])

    payment_obj = result["payment"]
    return PaymentResponse(
        payment_uuid=payment_obj.payment_uuid,
        account_uuid=payment_obj.account_uuid,
        amount=payment_obj.amount,
        description=payment_obj.description,
        status=result["status"]
    )
