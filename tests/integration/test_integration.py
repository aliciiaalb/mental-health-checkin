from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.main import app

client = TestClient(app)

import joblib
from pathlib import Path

def test_model_loading():
    model_path = Path(__file__).resolve().parents[2] / "mlflow" / "model" / "emotion_model.pkl"
    model = joblib.load(model_path)
    assert model is not None


def test_analyze_prediction():
    # Exemple de texte à analyser
    sample_input = {
        "message": "I feel really sad and tired today"
    }

    response = client.post("/analyze", json=sample_input)

    assert response.status_code == 200
    json_data = response.json()

    assert "predicted_emotion" in json_data
    assert isinstance(json_data["predicted_emotion"], str)
    assert len(json_data["predicted_emotion"]) > 0  # Doit renvoyer une émotion


def test_analyze_french_text():
    sample_input = {
        "message": "Je me sens heureux aujourd'hui"
    }

    response = client.post("/analyze", json=sample_input)

    assert response.status_code == 200
    assert "predicted_emotion" in response.json()
    assert "message" in response.json()
