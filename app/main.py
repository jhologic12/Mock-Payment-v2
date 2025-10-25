# app/main.py
from fastapi import FastAPI
from app.routers import account_router, card_router, payment_router
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.models import Account, Card, Payment
# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mock Payment API")

# Routers
app.include_router(account_router.router)
app.include_router(card_router.router)
app.include_router(payment_router.router)

# Permitir todos los orígenes (solo para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o lista de URLs de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)