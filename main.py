from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import joblib

# Charger le modèle (pipeline complet avec préprocessing)
model = joblib.load("model_final.joblib")

# Initialisation de l'app FastAPI
app = FastAPI(
    title="🚗 Getaround Pricing API",
    description="Prédiction du prix journalier d'une location en fonction des caractéristiques d'un véhicule.",
)

# Schéma de la requête
class PredictionRequest(BaseModel):
    input: List[Dict[str, Any]]

# Route principale de prédiction
@app.post("/predict")
def predict(data: PredictionRequest):
    input_df = pd.DataFrame(data.input)
    prediction = model.predict(input_df)
    return {"prediction": prediction.tolist()}

# Route d'accueil
@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API Getaround Pricing.",
        "info": "Utilisez /docs pour accéder à la documentation interactive Swagger."
    }
