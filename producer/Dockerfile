FROM python:3.12-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir pika

CMD ["python", "app.py"]
