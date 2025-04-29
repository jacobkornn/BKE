import os
import logging
import json
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize global objects
model = None
tfidf_vectorizer = None

def init():
    """
    This function is called when the container is initialized, typically after deployment.
    It loads the trained model and initializes necessary components for inference.
    """
    global model, tfidf_vectorizer
    
    model_dir = os.getenv("AZUREML_MODEL_DIR")
    model_path = os.path.join(model_dir, "jobTitlesRandomForestModel.pkl")
    vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")

    # Load the trained model
    model = joblib.load(model_path)
    
    # Load the trained TF-IDF vectorizer
    tfidf_vectorizer = joblib.load(vectorizer_path)
    
    logging.info("Model and vectorizer loaded successfully.")

def run(raw_data):
    """
    This function is called for each invocation of the endpoint.
    It extracts input data, preprocesses it, and returns predictions from the model.
    """
    try:
        logging.info("Request received")
        
        # Parse input JSON data
        data = json.loads(raw_data)
        job_titles = data["jobtitles"]
        
        # Transform job titles using the TF-IDF vectorizer
        X_tfidf = tfidf_vectorizer.transform(job_titles).toarray()
        
        # Feature Engineering
        def categorize_job_title(title):
            return [
                int(any(keyword in title for keyword in ["Technician", "Clerk", "Analyst"])),  # Individual Contributor
                int(any(keyword in title for keyword in ["Supervisor", "Lead"])),  # Lower Management
                int(any(keyword in title for keyword in ["Manager", "Superintendent"])),  # Middle Management
                int(any(keyword in title for keyword in ["Director", "Vice President", "President"])),  # Upper Management
                int(any(keyword in title for keyword in ["CEO", "CFO", "CTO", "Chief", "Executive"]))  # Executive
            ]

        features = np.array([categorize_job_title(title) for title in job_titles])
        
        # Combine TF-IDF features with categorical features
        X_final = np.hstack((X_tfidf, features))

        # Perform prediction
        predictions = model.predict(X_final).tolist()

        logging.info("Inference completed successfully")
        return json.dumps({"predictions": predictions})

    except Exception as e:
        logging.error(f"Error during inference: {str(e)}")
        return json.dumps({"error": str(e)})
