import joblib
import numpy as np
import json
import os
import csv
from azureml.core import Model
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from sklearn.feature_extraction.text import TfidfVectorizer

# Seniority mapping
SENIORITY_MAPPING = {
    0: "Individual Contributor",
    1: "Lower Management",
    2: "Middle Management",
    3: "Upper Management",
    4: "Executive"
}

# Load model and vectorizer using Azure ML SDK
def init():
    global model, vectorizer
    
    # Authenticate with Azure ML
    ml_client = MLClient(DefaultAzureCredential(), "c6eda382-a7f1-43d0-a66c-3b0ed8905988", "JakeGroup", "JakeWS-AzureSponsorship")
    
    # Retrieve model path from registered models
    model_path = Model.get_model_path("jobtitles_randomforest")
    
    # Retrieve vectorizer path as a data asset
    data_asset = ml_client.data.get(name="TF-IDF-vectorizer", version="1")
    vectorizer_path = data_asset.path

    # Load model and vectorizer
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

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