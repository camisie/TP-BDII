FROM python:3.10.6

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD ["python", "./migration.py"]
