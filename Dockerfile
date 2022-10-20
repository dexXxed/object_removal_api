FROM python:3.8

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 curl -y

WORKDIR /app
EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# copy project
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]