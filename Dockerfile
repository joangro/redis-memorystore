FROM python:3.7-alpine

WORKDIR /app
COPY . /app

RUN "pip install -r requirements.txt"

EXPOSE 8080
CMD ["python", "main.py"]
