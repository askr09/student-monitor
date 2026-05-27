# Student Monitoring and Risk Prediction System with Real-Time Monitoring

## Overview
An end-to-end MLOps project for real-time student risk prediction and monitoring, featuring:
- Flask ML API
- Prometheus metrics collection
- Grafana enterprise dashboards
- Jenkins CI/CD pipeline
- Dockerized deployment on AWS EC2

## Features
- Real-time API and ML monitoring
- System health and error tracking
- Automated build, test, deploy pipeline
- Scalable, secure AWS deployment

## Architecture
- Flask app exposes ML predictions and Prometheus metrics
- Prometheus scrapes Flask, Node Exporter, and itself
- Grafana visualizes all metrics
- Jenkins automates CI/CD
- All services run as Docker containers on AWS EC2

## Quick Start
1. Clone the repo
2. Update configs as needed
3. Run `docker-compose up -d`
4. Access:
   - Flask: `http://<EC2-IP>:5000`
   - Prometheus: `http://<EC2-IP>:9090`
   - Grafana: `http://<EC2-IP>:3000`
   - Jenkins: `http://<EC2-IP>:8080`

## Monitoring
- Dashboards: API requests, ML predictions, CPU/Memory, error rates, response times
- Real-time, enterprise-grade Grafana panels

## CI/CD
- Jenkinsfile for automated build, test, Docker build, deploy, and monitoring

## Deployment
- AWS EC2 (Ubuntu), Docker, Docker Compose
- Security groups for port management

## License
MIT
