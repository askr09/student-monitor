from flask import Flask, request, jsonify
from model import predict_student
import mysql.connector
import os

app = Flask(__name__)

# Required fields matching your dataset columns
REQUIRED_FIELDS = [
    'age', 'gender', 'study_hours_per_day', 'social_media_hours',
    'netflix_hours', 'part_time_job', 'attendance_percentage',
    'sleep_hours', 'diet_quality', 'exercise_frequency',
    'parental_education_level', 'internet_quality',
    'mental_health_rating', 'extracurricular_participation'
]

def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'password123'),
        database=os.getenv('DB_NAME', 'student_db')
    )

@app.route('/health')
def health():
    return jsonify({'status': 'running', 'model': 'Student Risk Predictor v1.0'})

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Validate all 14 fields are present
    for field in REQUIRED_FIELDS:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    result = predict_student(data)

    # Save to MySQL
    try:
        db  = get_db()
        cur = db.cursor()
        cur.execute('''INSERT INTO predictions (
            age, gender, study_hours_per_day, social_media_hours,
            netflix_hours, part_time_job, attendance_percentage,
            sleep_hours, diet_quality, exercise_frequency,
            parental_education_level, internet_quality,
            mental_health_rating, extracurricular_participation,
            risk_label, confidence)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (data['age'], data['gender'],
             data['study_hours_per_day'], data['social_media_hours'],
             data['netflix_hours'], data['part_time_job'],
             data['attendance_percentage'], data['sleep_hours'],
             data['diet_quality'], data['exercise_frequency'],
             data['parental_education_level'], data['internet_quality'],
             data['mental_health_rating'], data['extracurricular_participation'],
             result['risk_label'], result['confidence']))
        db.commit()
        cur.close(); db.close()
    except Exception as e:
        print(f'DB Error: {e}')

    return jsonify({
        'risk_label':  result['risk_label'],
        'confidence':  result['confidence'],
        'message':     'Prediction complete'
    })

@app.route('/api/predictions')
def all_predictions():
    try:
        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 100')
        rows = cur.fetchall()
        cur.close(); db.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
