import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/analyze", json={"message": "I feel fantastic!"})

    assert response.status_code == 200

    data = response.json()
    assert "predicted_emotion" in data
    assert isinstance(data["predicted_emotion"], str)
