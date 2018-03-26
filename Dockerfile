FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get --assume-yes install tesseract-ocr
ADD . /app/