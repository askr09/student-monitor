# Health check endpoint


from flask import Flask, request, jsonify, send_from_directory
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from model import predict_student
import mysql.connector
import os
import time


app = Flask(__name__)
from flask_cors import CORS
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')
# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
PREDICTION_COUNT = Counter('ml_predictions_total', 'Total ML Predictions', ['model', 'class'])
RESPONSE_TIME = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['endpoint'])
ACTIVE_USERS = Gauge('active_users', 'Number of Active Users')
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP Errors', ['endpoint', 'status'])

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


# --- Monitoring Middleware ---
@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_USERS.inc()

@app.after_request
def after_request(response):
    resp_time = time.time() - getattr(request, 'start_time', time.time())
    RESPONSE_TIME.labels(request.path).observe(resp_time)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    if response.status_code >= 400:
        ERROR_COUNT.labels(request.path, response.status_code).inc()
    ACTIVE_USERS.dec()
    return response

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print('Received data:', data)
    # Validate all 14 fields are present
    for field in REQUIRED_FIELDS:
        if field not in data:
            print(f'Missing field: {field}')
            return jsonify({'error': f'Missing field: {field}'}), 400

    result = predict_student(data)
    print('Prediction result:', result)
    # Prometheus ML prediction metric
    PREDICTION_COUNT.labels('student_model', result['risk_label']).inc()

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
        'message':     'Prediction complete',
        'debug': result.get('error') if isinstance(result, dict) and 'error' in result else None
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
    
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
