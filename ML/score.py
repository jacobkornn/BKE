# Import libraries
import joblib
import numpy as np
import json
import os
import csv
from azureml.core.model import Model

# Seniority mapping: numbers to labels
SENIORITY_MAPPING = {
    0: "Individual Contributor",
    1: "Lower Management",
    2: "Middle Management",
    3: "Upper Management",
    4: "Executive"
}

# Called when the service is loaded
def init():
    global model
    # Retrieve the path to the model file
    model_path = Model.get_model_path("jobTitlesRandomForestModel.pkl")
    model = joblib.load(model_path)

# Function to convert CSV to JSON and dynamically engineer features
def csv_to_json(csv_file_path):
    # Read the CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    # Transform data and engineer features
    json_data = {"data": [], "jobtitles": []}
    for row in data:
        json_data["jobtitles"].append(row["jobtitle"])  # Store job titles for printing
        features = [
            1 if any(title in row["jobtitle"] for title in ["Technician", "Clerk", "Analyst"]) else 0,
            1 if any(title in row["jobtitle"] for title in ["Supervisor", "Lead"]) else 0,
            1 if any(title in row["jobtitle"] for title in ["Manager", "Superintendent"]) else 0,
            1 if any(title in row["jobtitle"] for title in ["Director", "Vice President", "President"]) else 0,
            1 if any(title in row["jobtitle"] for title in ["CEO", "CFO", "CTO", "Chief", "Executive"]) else 0
        ]
        json_data["data"].append(features)
    
    return json_data

# Called when a request is received
def run(raw_data):
    try:
        # Parse input JSON data
        if raw_data.endswith(".csv"):  # If the input is a CSV file
            json_data = csv_to_json(raw_data)
        else:
            json_data = json.loads(raw_data)
        
        features = np.array(json_data["data"])
        jobtitles = json_data["jobtitles"]
        
        # Perform prediction
        predictions = model.predict(features)
        
        # Map numeric predictions to labels
        mapped_predictions = [SENIORITY_MAPPING[pred] for pred in predictions]
        
        # Combine job titles with predictions for formatted output
        result = []
        for jobtitle, seniority in zip(jobtitles, mapped_predictions):
            result.append(f"{jobtitle}: {seniority}")
        
        return {"predictions": result}
    except Exception as e:
        return {"error": str(e)}