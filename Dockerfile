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

# sudo gunicorn -D -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers 4 --timeout 5000 main:app
# sudo gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers 4 --timeout 5000 --access-logfile ./gpu_logs.log --log-file ./gpu_logs.log --log-level info --capture-output main:app