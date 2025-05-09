import joblib
import numpy as np
import json
import os
import csv
from azureml.core.model import Model
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
def init():
    global model, vectorizer
    model_path = Model.get_model_path("jobTitlesRandomForestModel.pkl")
    vectorizer_path = Model.get_model_path("tfidf_vectorizer.pkl")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

# Seniority mapping
SENIORITY_MAPPING = {0: "Individual Contributor", 1: "Lower Management", 2: "Middle Management", 3: "Upper Management", 4: "Executive"}

# Convert CSV input to JSON
def csv_to_json(csv_file_path):
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        jobtitles = [row["jobtitle"] for row in csv_reader]
    return {"jobtitles": jobtitles}

# Handle requests
def run(raw_data):
    try:
        if raw_data.endswith(".csv"):
            json_data = csv_to_json(raw_data)
        elif isinstance(raw_data, str):  
            json_data = {"jobtitles": [raw_data]}
        else:
            json_data = json.loads(raw_data)
        
        # Transform input using TF-IDF
        features = vectorizer.transform(json_data["jobtitles"])
        
        # Predict seniority
        predictions = model.predict(features)
        mapped_predictions = [SENIORITY_MAPPING[pred] for pred in predictions]

        result = [f"{jobtitle}: {seniority}" for jobtitle, seniority in zip(json_data["jobtitles"], mapped_predictions)]
        return {"predictions": result}
    except Exception as e:
        return {"error": str(e)}