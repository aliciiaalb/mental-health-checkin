import requests

def test_e2e_prediction():
    payload = {"message": "I hate everything"}  # <-- clé corrigée
    response = requests.post("http://localhost:8000/analyze", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "predicted_emotion" in result  # <-- corrige aussi ici
    assert result["predicted_emotion"] in [
        "anger", "joy", "sadness", "neutral", "disgust", "surprise",
        "love", "amusement", "embarrassment"
    ]

def test_invalid_field():
    payload = {"text": "I feel great"}  # Mauvaise clé, devrait être "message"
    response = requests.post("http://localhost:8000/analyze", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (FastAPI renvoie 422 pour les erreurs de validation)
    
def test_empty_message():
    payload = {"message": ""}
    response = requests.post("http://localhost:8000/analyze", json=payload)
    assert response.status_code == 200  # Si ton modèle accepte une chaîne vide
    result = response.json()
    assert "predicted_emotion" in result
