import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib
import mlflow
import mlflow.sklearn
import os

# 1. Chargement dataset (à adapter avec DVC plus tard)
df = pd.read_csv("data/goemotions.csv",quotechar='"')
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
df = df[df['emotion'].notnull()]
X = df['text']
y = df['emotion']

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=300))
])

# 4. MLflow
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("goemotions-baseline")

with mlflow.start_run():
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Exemple : f1-score pour "joy"
    mlflow.log_metric("f1_joy", report.get("joy", {}).get("f1-score", 0.0))

    input_example = pd.DataFrame({"text": ["I'm happy today!"]})
    
    # Enregistrement du modèle
    mlflow.sklearn.log_model(pipeline, "model", registered_model_name="goemotions-model", input_example=input_example)
    joblib.dump(pipeline, "mlflow/model/emotion_model.pkl")
