from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.card_schema import CardCreate, CardResponse
from app.services.card_service import create_card, validate_card
from app.database import get_db
from app.schemas.card_schema import CardValidationRequest
from app.services.card_service import validate_card_internal


router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/", response_model=CardResponse)
def create_card_endpoint(card: CardCreate, db: Session = Depends(get_db)):
    return create_card(db, card)




@router.post("/validate")
def validate_card_endpoint(request: CardValidationRequest, db: Session = Depends(get_db)):
    """
    Endpoint interno para validar tarjeta:
    - Recibe todos los datos de la tarjeta.
    - Devuelve datos internos si todo coincide.
    - Mensaje genérico si falla.
    """
    result = validate_card_internal(
        db,
        card_number=request.card_number,
        holder_name=request.holder_name,
        expiration_date=request.expiration_date,
        cvv=request.cvv
    )
    return result
