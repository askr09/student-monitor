import joblib
import numpy as np

# Load model
model = joblib.load('model/model.pkl')
FEATURES = joblib.load('model/features.pkl')

GENDER_MAP = {'Female': 0, 'Male': 1, 'Other': 2}
YESNO_MAP = {'No': 0, 'Yes': 1}
DIET_MAP = {'Fair': 0, 'Good': 1, 'Poor': 2}
PARENT_EDU_MAP = {'Bachelor': 0, 'High School': 1, 'Master': 2, 'Unknown': 3}
INTERNET_MAP = {'Average': 0, 'Good': 1, 'Poor': 2}

def predict_student(data: dict) -> dict:
    features = [
        data['age'],
        GENDER_MAP.get(data['gender'], 1),
        data['study_hours_per_day'],
        data['social_media_hours'],
        data['netflix_hours'],
        YESNO_MAP.get(data['part_time_job'], 0),
        data['attendance_percentage'],
        data['sleep_hours'],
        DIET_MAP.get(data['diet_quality'], 0),
        data['exercise_frequency'],
        PARENT_EDU_MAP.get(data['parental_education_level'], 3),
        INTERNET_MAP.get(data['internet_quality'], 0),
        data['mental_health_rating'],
        YESNO_MAP.get(data['extracurricular_participation'], 0),
    ]

    X = np.array([features])
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0].max()

    return {
        'risk_label': prediction,
        'confidence': round(float(confidence) * 100, 2)
    }