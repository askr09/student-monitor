pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'student-monitoring-app:latest'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps {
                sh 'pip install --break-system-packages --only-binary=:all: -r app/requirements.txt'

                sh 'python3 -m pytest app/ || true'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }
        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker tag $DOCKER_IMAGE $USER/$DOCKER_IMAGE'
                    sh 'docker push $USER/$DOCKER_IMAGE'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }
        stage('Monitoring') {
            steps {
                sh 'curl -f http://localhost:5000/metrics'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
