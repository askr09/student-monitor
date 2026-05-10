CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS predictions (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    age                         INT,
    gender                      VARCHAR(10),
    study_hours_per_day         FLOAT,
    social_media_hours          FLOAT,
    netflix_hours               FLOAT,
    part_time_job               VARCHAR(5),
    attendance_percentage       FLOAT,
    sleep_hours                 FLOAT,
    diet_quality                VARCHAR(10),
    exercise_frequency          INT,
    parental_education_level    VARCHAR(20),
    internet_quality            VARCHAR(10),
    mental_health_rating        INT,
    extracurricular_participation VARCHAR(5),
    risk_label                  VARCHAR(10),
    confidence                  FLOAT,
    created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
