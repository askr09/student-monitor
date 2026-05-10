import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print('Loading dataset...')
df = pd.read_csv('data/students.csv')
print(f'Dataset loaded: {df.shape[0]} students, {df.shape[1]} columns')

# ── STEP 1: Convert exam_score to risk label ──────────────
# At Risk = below 40, Average = 40-60, Safe = above 60
def score_to_label(score):
    if score < 40:
        return 'At Risk'
    elif score < 60:
        return 'Average'
    else:
        return 'Safe'

df['risk_label'] = df['exam_score'].apply(score_to_label)
print('\nRisk label distribution:')
print(df['risk_label'].value_counts())

# ── STEP 2: Encode categorical columns ────────────────────
# Convert text columns to numbers for ML
le = LabelEncoder()

df['gender_enc']              = le.fit_transform(df['gender'])
df['part_time_job_enc']       = le.fit_transform(df['part_time_job'])
df['diet_quality_enc']        = le.fit_transform(df['diet_quality'])
df['parental_edu_enc']        = le.fit_transform(df['parental_education_level'])
df['internet_quality_enc']    = le.fit_transform(df['internet_quality'])
df['extracurricular_enc']     = le.fit_transform(df['extracurricular_participation'])

# ── STEP 3: Select features ───────────────────────────────
df['study_efficiency'] = df['study_hours_per_day'] / (df['social_media_hours'] + df['netflix_hours'] + 1)
FEATURES = [
    'age',
    'gender_enc',
    'study_hours_per_day',
    'social_media_hours',
    'netflix_hours',
    'part_time_job_enc',
    'attendance_percentage',
    'sleep_hours',
    'diet_quality_enc',
    'exercise_frequency',
    'parental_edu_enc',
    'internet_quality_enc',
    'mental_health_rating',
    'extracurricular_enc',
]
FEATURES.append('study_efficiency')

X = df[FEATURES]
y = df['risk_label']

# ── STEP 4: Split data ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f'\nTraining samples: {len(X_train)}')
print(f'Testing samples:  {len(X_test)}')

# ── STEP 5: Train model ───────────────────────────────────
print('\nTraining Random Forest model...')
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    # min_samples_split=10,
    # min_samples_leaf=4,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# ── STEP 6: Evaluate ──────────────────────────────────────
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'\nModel Accuracy: {accuracy * 100:.2f}%')
print('\nDetailed Report:')
print(classification_report(y_test, predictions))

# ── STEP 7: Feature importance ────────────────────────────
importance = pd.DataFrame({
    'feature': FEATURES,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print('\nTop 5 most important features:')
print(importance.head())

# ── STEP 8: Save model ────────────────────────────────────
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/model.pkl')
joblib.dump(FEATURES, 'model/features.pkl')
print('\nModel saved to model/model.pkl')
print('Features saved to model/features.pkl')
