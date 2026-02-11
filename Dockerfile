# 1. Base image
FROM python:3.11-slim

# 2. Working directory
WORKDIR /app

# 3. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. System dependencies (opsiyonel ama önerilir)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Application code
COPY app ./app

# 7. Expose port
EXPOSE 8000

# 8. Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
