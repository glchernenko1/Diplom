FROM python:3.8

RUN apt-get update &&\
    apt-get install -y python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /src
COPY downloader.py /

WORKDIR /