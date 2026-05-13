from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import joblib
import json
import numpy as np
import os

app = FastAPI(title="AI Health Symptom Checker API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load resources
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model_path = os.path.join(BASE_DIR, 'models', 'health_model.pkl')
    symptom_list_path = os.path.join(BASE_DIR, 'models', 'symptom_list.pkl')
    disease_info_path = os.path.join(BASE_DIR, 'data', 'disease_info.json')
    
    model = joblib.load(model_path)
    symptom_list = joblib.load(symptom_list_path)
    with open(disease_info_path, 'r') as f:
        disease_info = json.load(f)
except Exception as e:
    print(f"Error loading model/data: {e}")
    model = None
    symptom_list = []
    disease_info = {}

class SymptomRequest(BaseModel):
    symptoms: List[str]

@app.get("/")
async def root():
    return {
        "status": "online", 
        "message": "HealthCheck AI API is running successfully!",
        "endpoints": ["/symptoms", "/predict"]
    }

@app.get("/symptoms")
async def get_symptom_list():
    return {"symptoms": symptom_list}

@app.post("/predict")
async def predict(request: SymptomRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    # Create input vector
    input_vector = np.zeros(len(symptom_list))
    for sym in request.symptoms:
        if sym in symptom_list:
            idx = symptom_list.index(sym)
            input_vector[idx] = 1
    
    # Predict probabilities
    probs = model.predict_proba([input_vector])[0]
    classes = model.classes_
    
    # Get top 3 predictions
    top_indices = np.argsort(probs)[-3:][::-1]
    
    results = []
    for idx in top_indices:
        prob = float(probs[idx])
        if prob > 0:
            disease = classes[idx]
            info = disease_info.get(disease, {
                "severity": "Unknown", 
                "description": "", 
                "precautions": [], 
                "health_advice": ""
            })
            results.append({
                "disease": disease,
                "confidence": round(prob * 100, 2),
                "severity": info["severity"],
                "description": info["description"],
                "precautions": info["precautions"],
                "health_advice": info["health_advice"]
            })
    
    if not results:
        return {"predictions": [], "message": "No specific matches found. Please consult a doctor."}

    return {"predictions": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
