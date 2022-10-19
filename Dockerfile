FROM python:3.8

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 curl -y

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . .