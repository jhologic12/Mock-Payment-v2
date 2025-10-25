# app/test_db_connection.py
from app.database import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print("✅ Conexión exitosa a la base de datos")
            print(f"PostgreSQL version: {version[0]}")
    except Exception as e:
        print("❌ Error al conectar con la base de datos")
        print(e)

if __name__ == "__main__":
    test_connection()
