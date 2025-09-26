import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env (коментарі українською мовою)
load_dotenv()

# URL бази даних, наприклад: postgresql+psycopg2://user:pass@localhost:5432/contacts_db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")

# Ініціалізація синхронного двигуна SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Фабрика сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Повертає сесію БД для залежностей FastAPI. Закриває сесію після використання.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()