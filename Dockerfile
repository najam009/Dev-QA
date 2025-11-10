# Base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first
COPY requirements.txt .

# Upgrade pip to latest first (prevents old build logic issues)
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of your project files
COPY . .

# ✅ Create the folder to avoid watchdog FileNotFoundError
RUN mkdir -p /home/najam/S3bucket

# Set app port
ARG APP_PORT=3000
ENV APP_PORT=$APP_PORT
EXPOSE $APP_PORT

# Default run command
CMD ["python", "s3_database.py"]
