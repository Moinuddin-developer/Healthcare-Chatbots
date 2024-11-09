from fastapi import FastAPI
from pydantic import BaseModel
from typing import List  # Import List from typing for compatibility with Python 3.8

app = FastAPI()

# Define disease data with additional fields
diseases_info = {
    "diabetes": {
        "symptoms": ["Frequent urination", "Increased thirst", "Extreme hunger", "Fatigue"],
        "exercise": "Engage in moderate-intensity activities such as brisk walking or cycling for 30 minutes daily.",
        "sleep_hours": "7-8 hours per night to improve blood sugar levels and manage stress.",
        "diet": "Low-carb, high-fiber foods, avoid processed sugars and saturated fats.",
        "description": "A chronic condition that affects how your body processes blood sugar.",
        "treatment": "Regular exercise, healthy diet, and insulin therapy."
    },
    "hypertension": {
        "symptoms": ["Headache", "Shortness of breath", "Nosebleeds", "Fatigue"],
        "exercise": "30-40 minutes of moderate aerobic exercises like walking, swimming, or cycling.",
        "sleep_hours": "7-9 hours to help regulate blood pressure levels.",
        "diet": "Low-sodium diet, rich in fruits, vegetables, whole grains, and lean proteins.",
        "description": "High blood pressure, often with no symptoms but can lead to severe health issues.",
        "treatment": "Medication, lifestyle changes, and regular monitoring."
    },
    "heart disease": {
        "symptoms": ["Chest pain", "Shortness of breath", "Pain in neck/jaw", "Fatigue"],
        "exercise": "Regular low-intensity exercises, such as walking or yoga, for 30 minutes most days.",
        "sleep_hours": "7-9 hours to support heart health.",
        "diet": "Mediterranean diet with lots of fruits, vegetables, whole grains, and healthy fats.",
        "description": "A range of conditions that affect the heart, including coronary artery disease.",
        "treatment": "Medications, lifestyle changes, and possibly surgery."
    },
    "asthma": {
        "symptoms": ["Shortness of breath", "Chest tightness", "Wheezing", "Coughing"],
        "exercise": "Breathing exercises, light aerobic activities, but avoid outdoor activities in cold weather.",
        "sleep_hours": "7-8 hours to help reduce inflammation and maintain respiratory health.",
        "diet": "Anti-inflammatory diet with leafy greens, nuts, and healthy oils; avoid processed foods.",
        "description": "A condition where airways narrow and swell, producing extra mucus.",
        "treatment": "Inhalers, medication, and avoiding triggers."
    }
}

# Define request and response models
class DiseaseRequest(BaseModel):
    disease: str

class DiseaseResponse(BaseModel):
    description: str
    symptoms: List[str]  # Use List[str] instead of list[str] for compatibility with Python 3.8
    treatment: str
    exercise: str
    sleep_hours: str
    diet: str

# Define an endpoint for retrieving disease information
@app.post("/get_disease_info", response_model=DiseaseResponse)
async def get_disease_info(request: DiseaseRequest):
    disease = request.disease.lower()
    if disease in diseases_info:
        return diseases_info[disease]
    return {
        "description": "Disease not found",
        "symptoms": [],
        "treatment": "",
        "exercise": "No specific recommendations",
        "sleep_hours": "No specific recommendations",
        "diet": "No specific recommendations"
    }

# Sample health advice endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Chatbot API"}
