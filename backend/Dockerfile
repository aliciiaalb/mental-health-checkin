FROM python:3.10-slim

WORKDIR /app

# Copier tout le backend
COPY . .
# Copier le modèle (chemin relatif au contexte .)
COPY mlflow/model/emotion_model.pkl ./mlflow/model/emotion_model.pkl

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
