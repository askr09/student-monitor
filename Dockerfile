FROM python:3.11-slim
WORKDIR /app

COPY app/requirements.txt .

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY app/ .
COPY model/ ./model/

EXPOSE 5000
CMD ["python", "app.py"]