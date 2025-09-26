# Базовий образ
FROM python:3.12-slim

# Встановлення залежностей системи для psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо вихідний код
COPY app ./app
COPY .env ./.env

# Експонуємо порт
EXPOSE 8000

# Команда запуску
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]