FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data/ ./data/
COPY model.pkl .
COPY app.py .

EXPOSE 6000
CMD ["python", "app.py"]
