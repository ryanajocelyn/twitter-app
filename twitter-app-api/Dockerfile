FROM python:3.8-slim-buster

WORKDIR /usr/app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]