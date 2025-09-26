import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import text
from .database import engine
from .models import Base
from .routers import contacts

# Завантаження .env на старті (зручно для локальної розробки)
load_dotenv()

app = FastAPI(
    title="Contacts API",
    description="Простий REST API для управління контактами (FastAPI + SQLAlchemy + PostgreSQL)",
    version="1.0.0"
)

# Ініціалізуємо таблиці, якщо їх немає (для простоти без Alembic)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Підключаємо роутер контактів
app.include_router(contacts.router)

@app.get("/", tags=["health"])
def healthcheck():
    # Проста перевірка стану сервісу
    return {"status": "ok"}