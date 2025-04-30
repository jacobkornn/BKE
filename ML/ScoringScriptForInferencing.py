import json
import joblib
import numpy as np

# Initialization function
def init():
    global model, tfidf_vectorizer
    # Load the Random Forest model
    model_path = Model.get_model_path("JobTitles-RandomForrest")
    model = joblib.load(model_path)
    # Load the saved TF-IDF vectorizer
    tfidf_path = "tfidf_vectorizer.joblib"
    tfidf_vectorizer = joblib.load(tfidf_path)

# Function for feature engineering during inference
def process_features(job_titles):
    tfidf_features = tfidf_vectorizer.transform(job_titles).toarray()
    engineered_features = np.array([
        [
            1 if any(title in jt for title in ['Technician', 'Clerk', 'Analyst']) else 0,
            1 if any(title in jt for title in ['Supervisor', 'Lead']) else 0,
            1 if any(title in jt for title in ['Manager', 'Superintendent']) else 0,
            1 if any(title in jt for title in ['Director', 'Vice President', 'President']) else 0,
            1 if any(title in jt for title in ['CEO', 'CFO', 'CTO', 'Chief', 'Executive']) else 0
        ]
        for jt in job_titles
    ])
    return np.hstack((tfidf_features, engineered_features))

# Run function
def run(raw_data):
    try:
        # Parse input JSON
        data = json.loads(raw_data)
        job_titles = data["jobtitle"]  # Ensure input JSON includes a "jobtitle" key
        # Process features
        input_features = process_features(job_titles)
        # Make predictions
        predictions = model.predict(input_features)
        return predictions.tolist()
    except Exception as e:
        return {"error": str(e)}