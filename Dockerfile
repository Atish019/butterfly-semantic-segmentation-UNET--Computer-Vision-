# Base Image
FROM python:3.9-slim

# Set Working Directory
WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy & Install Requirements
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY backend/ backend/
COPY frontend/ frontend/
COPY saved_model/ saved_model/
COPY app.py .

# Environment Variables
ENV PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2

# Expose FastAPI Port
EXPOSE 8000

# Run Application
CMD ["python", "app.py"]
