FROM python:3.8
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y chromium chromium-driver
RUN pip install -r requirements.txt
ENV PORT=8080
CMD exec gunicorn --bind :$PORT app:app
