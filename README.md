# Contacts API (FastAPI + SQLAlchemy + PostgreSQL)

Простий REST API для зберігання та управління контактами. Підтримує CRUD-операції, пошук за ім'ям/прізвищем/email та вибірку контактів з днями народження у найближчі 7 днів.

## Стек
- FastAPI
- SQLAlchemy 2.0 (ORM)
- PostgreSQL
- Pydantic v2
- Uvicorn
- python-dotenv

## Швидкий старт (локально)

1. Створіть і заповніть `.env` на основі `.env.example`:
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/contacts_db
   ```
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустіть сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Документація:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Docker
Якщо у вас вже є контейнер з PostgreSQL, просто вкажіть коректний `DATABASE_URL` у `.env`.

Запуск API у Docker:
```bash
cp .env.example .env  # відредагуйте під свій Postgres
docker build -t contacts-api .
docker run --env-file .env -p 8000:8000 --name contacts_api contacts-api
```

**docker-compose** (приклад файлу вже додано):
```bash
docker compose up -d --build
```

## Маршрути
- `POST /contacts` — створити контакт
- `GET /contacts` — список контактів (параметри: `skip`, `limit`, `first_name`, `last_name`, `email`)
- `GET /contacts/{id}` — отримати контакт за ID
- `PUT /contacts/{id}` — оновити контакт
- `DELETE /contacts/{id}` — видалити контакт
- `GET /contacts/birthdays/upcoming?days=7` — дні народження в найближчі N днів

## Нотатки з безпеки
- Не зберігайте секрети в репозиторії. Використовуйте `.env` або менеджери секретів.
- Для продакшну використовуйте Alembic міграції. Тут для простоти ініціалізація таблиць відбувається на старті.

## Ліцензія
MIT# goit-pythonweb-hw-08
