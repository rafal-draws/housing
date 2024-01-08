FROM python:latest

USER root

WORKDIR /app

COPY /app .


RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get install -y firefox-esr

CMD ["python", "main.py", "csv", "/app/data", "firefox"]