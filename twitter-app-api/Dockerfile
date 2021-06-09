FROM python:3.8-slim-buster

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -qq install libmariadb-dev-compat libmariadb-dev gcc

WORKDIR /usr/app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]