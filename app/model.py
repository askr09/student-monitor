import joblib
import numpy as np

# Load model
model = joblib.load('model/model.pkl')
FEATURES = joblib.load('model/features.pkl')

# Updated mappings to match frontend values
GENDER_MAP = {'Female': 0, 'Male': 1, 'Other': 2}
YESNO_MAP = {'No': 0, 'Yes': 1}
DIET_MAP = {'Poor': 0, 'Average': 1, 'Good': 2}
PARENT_EDU_MAP = {
    'None': 0, 'High School': 1, 'Bachelor': 2, 'Master': 3, 'PhD': 4
}
INTERNET_MAP = {'Poor': 0, 'Average': 1, 'Good': 2}
EXERCISE_MAP = {
    'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3, 'Always': 4
}
MENTAL_HEALTH_MAP = {
    'Poor': 0, 'Average': 1, 'Good': 2, 'Excellent': 3
}

def predict_student(data: dict) -> dict:
    try:
        features = [
            int(data['age']),
            GENDER_MAP[data['gender']],
            int(data['study_hours_per_day']),
            int(data['social_media_hours']),
            int(data['netflix_hours']),
            YESNO_MAP[data['part_time_job']],
            int(data['attendance_percentage']),
            int(data['sleep_hours']),
            DIET_MAP[data['diet_quality']],
            EXERCISE_MAP[data['exercise_frequency']],
            PARENT_EDU_MAP[data['parental_education_level']],
            INTERNET_MAP[data['internet_quality']],
            MENTAL_HEALTH_MAP[data['mental_health_rating']],
            YESNO_MAP[data['extracurricular_participation']],
        ]
    except Exception as e:
        return {'risk_label': 'Error', 'confidence': 0, 'error': f'Feature mapping error: {e}'}

    X = np.array([features])
    try:
        prediction = model.predict(X)[0]
        confidence = model.predict_proba(X)[0].max()
    except Exception as e:
        return {'risk_label': 'Error', 'confidence': 0, 'error': f'Model prediction error: {e}'}

    return {
        'risk_label': prediction,
        'confidence': round(float(confidence) * 100, 2)
    }