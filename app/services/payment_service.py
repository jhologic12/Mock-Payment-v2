# app/services/payment_service.py
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.models.account import Account

def create_payment(db: Session, payment_data):
    account = db.query(Account).filter(Account.account_uuid == str(payment_data.account_uuid)).first()
    if not account:
        return {"status": "rechazado", "message": "Cuenta no encontrada"}

    if account.balance < payment_data.amount:
        return {"status": "rechazado", "message": "Saldo insuficiente"}

    account.balance -= payment_data.amount
    payment = Payment(
        account_uuid=str(payment_data.account_uuid),
        amount=payment_data.amount,
        description=payment_data.description
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {"status": "aprobado", "payment": payment, "balance_restante": account.balance}
