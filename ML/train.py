import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# Load data
jobTitles = pd.read_csv('jobtitles_train.csv')

# Feature Engineering
jobTitles['is_individual_contributor'] = jobTitles['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Technician', 'Clerk', 'Analyst']) else 0)
jobTitles['is_lower_management'] = jobTitles['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Supervisor', 'Lead']) else 0)
jobTitles['is_middle_management'] = jobTitles['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Manager', 'Superintendent']) else 0)
jobTitles['is_upper_management'] = jobTitles['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['Director', 'Vice President', 'President']) else 0)
jobTitles['is_exec'] = jobTitles['jobtitle'].apply(lambda x: 1 if any(title in x for title in ['CEO', 'CFO', 'CTO', 'Chief', 'Executive']) else 0)

# Define features (only the binary features)
X = jobTitles[['is_individual_contributor', 'is_lower_management', 'is_middle_management', 'is_upper_management', 'is_exec']].values

# Define the categories for seniority
seniority_mapping = {
    'Individual Contributor': 0,
    'Lower Management': 1,
    'Middle Management': 2,
    'Upper Management': 3,
    'Executive': 4
}
jobTitles['seniority'] = jobTitles['seniority'].map(seniority_mapping)

# Split data into features and target
y = jobTitles['seniority']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

# Initialize and train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, 'jobTitlesRandomForestModel.pkl')