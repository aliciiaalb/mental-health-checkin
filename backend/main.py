# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel  
import joblib
import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware


# Charger le modèle au lancement de l'API
MODEL_PATH = "mlflow/model/emotion_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")

# Initialiser FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou précise ["http://localhost:5173"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Définir le format de la requête
class TextInput(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"message": "Mental Health Check-in API is live!"}

# Définir le endpoint
@app.post("/analyze")
def analyze_emotion(text: TextInput):
    try:
        prediction = model.predict([text.message])[0]
        return {
            "message": text.message,
            "predicted_emotion": prediction
        }
    except Exception as e:
        return {
            "error": str(e)
        }
