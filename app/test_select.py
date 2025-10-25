from app.database import SessionLocal
from app.models import Account

def main():
    db = SessionLocal()
    accounts = db.query(Account).all()
    if accounts:
        print("Se encontraron registros:")
        for acc in accounts:
            print(f"UUID: {acc.account_uuid} | Owner: {acc.owner_name} | Account Number: {acc.account_number} | Balance: {acc.balance}")
    else:
        print("No se encontraron registros")
    db.close()

if __name__ == "__main__":
    main()
