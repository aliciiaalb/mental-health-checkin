import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.main import app

client = TestClient(app)

# tests/unit/test_model_prediction.py

import joblib
from pathlib import Path

def test_model_prediction_label():
    model_path = Path(__file__).resolve().parents[2] / "mlflow" / "model" / "emotion_model.pkl"
    model = joblib.load(model_path)
    prediction = model.predict(["I am very happy today"])[0]
    assert isinstance(prediction, str)
    assert prediction in ["anger", "joy", "sadness", "neutral", "disgust", "surprise", "love", "amusement", "embarrassment"]


def test_analyze_endpoint():
    response = client.post("/analyze", json={"message": "I feel fantastic!"})

    assert response.status_code == 200

    data = response.json()
    assert "predicted_emotion" in data
    assert isinstance(data["predicted_emotion"], str)
