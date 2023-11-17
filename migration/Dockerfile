FROM python:3.10.6

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y postgresql-client

CMD ["sh", "./setup.sh"]

