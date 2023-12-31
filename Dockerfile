FROM python:3.9-slim

WORKDIR /app

COPY . /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


CMD ["python", "main.py"]
