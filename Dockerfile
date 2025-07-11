FROM python:3.10-slim

# Backend
WORKDIR /app
COPY backend/ /app/
COPY backend/mlflow/model/emotion_model.pkl /app/mlflow/model/emotion_model.pkl

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Frontend
WORKDIR /frontend
COPY frontend/ /frontend/
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install && npm run build

# Move built frontend into backend static files (optional, if backend serves it)
# RUN mv build /app/static

# Final command
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
