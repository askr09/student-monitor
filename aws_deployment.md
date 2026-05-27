# AWS EC2 Deployment Steps

1. Launch an Ubuntu EC2 instance (t2.medium+ recommended).
2. Open ports in the security group: 22 (SSH), 5000 (Flask), 9090 (Prometheus), 3000 (Grafana), 8080 (Jenkins), 9100 (Node Exporter).
3. SSH into the instance.
4. Install Docker and Docker Compose:
   - `sudo apt update && sudo apt install -y docker.io docker-compose`
   - `sudo usermod -aG docker $USER && newgrp docker`
5. Clone your project repo.
6. Run: `docker-compose up -d`
7. Access services via EC2 public IP and respective ports.

# Security Groups
- Only open required ports to the internet.
- Restrict SSH (22) to your IP.
- Allow 5000, 9090, 3000, 8080, 9100 as needed for demo/monitoring.

# Architecture Diagram (Text)

```
+-------------------+
|    AWS EC2 VM     |
|-------------------|
|  Docker Compose   |
|-------------------|
| Flask (5000)      |
| Prometheus (9090) |
| Grafana (3000)    |
| Jenkins (8080)    |
| Node Exporter     |
+-------------------+
```

- Prometheus scrapes Flask, Node Exporter, and itself.
- Grafana visualizes Prometheus data.
- Jenkins manages CI/CD.
- All services are containerized.
