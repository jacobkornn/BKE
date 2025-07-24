import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Load data
jobTitles = pd.read_csv('jobtitles_train.csv')

# Define the categories for seniority
seniority_mapping = {
    'Individual Contributor': 0,
    'Lower Management': 1,
    'Middle Management': 2,
    'Upper Management': 3,
    'Executive': 4
}
jobTitles['seniority'] = jobTitles['seniority'].map(seniority_mapping)

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(jobTitles['jobtitle'])

# Target variable
y = jobTitles['seniority']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model and vectorizer
joblib.dump(model, 'jobTitlesRandomForestModel.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')