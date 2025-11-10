# Base image
FROM python:3.10-slim

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ..

ARG APP_PORT=3000
ENV APP_PORT=$APP_PORT

EXPOSE $APP_PORT

CMD ["python", "s3_database.py"]
