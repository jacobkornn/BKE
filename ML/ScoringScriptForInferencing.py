import json
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Global variables for model and vectorizer
model = None
tfidf = None

def init():
    """Initialize the model and vectorizer by loading them from disk."""
    global model, tfidf
    model = joblib.load('jobTitlesRandomForestModel.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')

def run(raw_data):
    """Run inference on the input job titles."""
    try:
        # Parse incoming JSON request
        job_titles = json.loads(raw_data)['job_titles']
        jobTitles_df = pd.DataFrame({'jobtitle': job_titles})

        # Apply TF-IDF transformation
        X_tfidf = tfidf.transform(jobTitles_df['jobtitle'])

        # Feature Engineering (same logic as training)
        jobTitles_df['is_individual_contributor'] = jobTitles_df['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Technician', 'Clerk', 'Analyst']) else 0)
        jobTitles_df['is_lower_management'] = jobTitles_df['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Supervisor', 'Lead']) else 0)
        jobTitles_df['is_middle_management'] = jobTitles_df['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Manager', 'Superintendent']) else 0)
        jobTitles_df['is_upper_management'] = jobTitles_df['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Director', 'Vice President', 'President']) else 0)
        jobTitles_df['is_exec'] = jobTitles_df['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['CEO', 'CFO', 'CTO', 'Chief', 'Executive']) else 0)

        # Combine features
        X = np.hstack((X_tfidf.toarray(), jobTitles_df[['is_individual_contributor', 'is_lower_management', 'is_middle_management', 'is_upper_management', 'is_exec']].values))

        # Make predictions
        predictions = model.predict(X)

        # Convert numeric predictions to labels
        seniority_mapping = {0: 'Individual Contributor', 1: 'Lower Management', 2: 'Middle Management', 3: 'Upper Management', 4: 'Executive'}
        predicted_labels = [seniority_mapping[pred] for pred in predictions]

        return json.dumps({"predictions": predicted_labels})

    except Exception as e:
        return json.dumps({"error": str(e)})
