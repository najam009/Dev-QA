# Base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining source code
COPY . .

# App port (optional)
ARG APP_PORT=3000
ENV APP_PORT=$APP_PORT
EXPOSE $APP_PORT

# Run your app
CMD ["python", "s3_database.py"]
