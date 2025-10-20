from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.card import Card
from app.models.account import Account
from app.schemas.card_schema import CardCreate, CardResponse, AccountInfo, CardInfo
import logging

logger = logging.getLogger(__name__)

def validate_card_internal(db: Session, card_number: str, holder_name: str, expiration_date: str, cvv: str) -> dict:
    """
    Valida todos los campos de la tarjeta en la DB.
    Retorna datos internos para el flujo de pago si es correcto.
    Responde genérico si algo falla.
    """
    card_number = card_number.replace(" ", "")
    holder_name = holder_name.strip()
    expiration_date = expiration_date.strip()
    cvv = cvv.strip()

    card: Card | None = db.query(Card).filter(Card.card_number == card_number).first()
    if not card:
        logger.info("Validación tarjeta: no encontrada")
        raise HTTPException(status_code=400, detail="Los datos de la tarjeta no son válidos")

    # Comparación de campos
    if card.holder_name.strip() != holder_name \
       or card.expiration_date.strip() != expiration_date \
       or card.cvv.strip() != cvv:
        logger.info("Validación tarjeta: datos incorrectos")
        raise HTTPException(status_code=400, detail="Los datos de la tarjeta no son válidos")

    # Obtener cuenta asociada
    account: Account | None = db.query(Account).filter(Account.account_uuid == card.account_uuid).first()
    if not account:
        logger.error("Cuenta asociada no encontrada para tarjeta")
        raise HTTPException(status_code=400, detail="Los datos de la tarjeta no son válidos")

    logger.info("Validación tarjeta: OK")
    return {
        "card_number": card.card_number,
        "account_uuid": account.account_uuid,
        "account_number": account.account_number
    }


def create_card(db: Session, card_data: CardCreate) -> CardResponse:
    # Verificar que la cuenta existe
    account = db.query(Account).filter(Account.account_uuid == card_data.account_uuid).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Crear tarjeta vinculada a la cuenta
    new_card = Card(
        account_uuid=account.account_uuid,
        card_number=card_data.card_number,
        holder_name=card_data.holder_name,
        expiration_date=card_data.expiration_date,
        cvv=card_data.cvv
    )

    db.add(new_card)
    try:
        db.commit()
        db.refresh(new_card)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Card number already exists")

    # Últimos 4 dígitos
    last4 = new_card.card_number[-4:]

    # Construir lista de tarjetas de la cuenta
    cards_info = [
        CardInfo(
            card_uuid=card.card_uuid,
            last4=card.card_number[-4:],
            holder_name=card.holder_name,
            expiration_date=card.expiration_date
        )
        for card in account.cards
    ]

    # Información completa de la cuenta
    account_info = AccountInfo(
        account_uuid=account.account_uuid,
        owner_name=account.owner_name,
        account_number=account.account_number,
        cards=cards_info
    )

    return CardResponse(
        card_uuid=new_card.card_uuid,
        account_uuid=new_card.account_uuid,
        holder_name=new_card.holder_name,
        expiration_date=new_card.expiration_date,
        last4=last4,
        account=account_info
    )


def validate_card(db: Session, card_number: str) -> dict:
    card = db.query(Card).filter(Card.card_number == card_number).first()
    if not card:
        return {"exists": False, "message": "Card not found"}
    return {"exists": True, "message": "Card exists", "card_uuid": card.card_uuid}
