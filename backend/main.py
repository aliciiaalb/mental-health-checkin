# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# Charger le modèle au lancement de l'API
MODEL_PATH = os.path.join("mlflow", "model", "emotion_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")

# Initialiser FastAPI
app = FastAPI()

# Définir le format de la requête
class TextInput(BaseModel):
    message: str

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
