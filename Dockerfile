# Base image
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ARG APP_PORT=3000
ENV APP_PORT=$APP_PORT

EXPOSE $APP_PORT

CMD ["python", "s3_database.py"]
