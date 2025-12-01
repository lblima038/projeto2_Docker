FROM python:3.11-slim

WORKDIR /app

# SQLite já vem com Python, não precisa instalar nada
COPY init_db.py .

CMD ["python", "init_db.py"]

