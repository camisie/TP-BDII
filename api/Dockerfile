FROM python:3.11

COPY . /api
WORKDIR /api

RUN pip install -r ./requirements.txt
RUN apt-get update && \
    apt-get install -y postgresql-client
EXPOSE 8000
CMD ["sh", "./wait_bds.sh"]
