FROM python:3.10-slim

WORKDIR /app

# Copier tout le backend et les fichiers nécessaires
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
