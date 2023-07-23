FROM python:3.9-slim-buster as backend
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE $PORT
RUN apt-get update -y

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY ./requirements.txt .
COPY ./install_requirement.sh .

RUN ./install_requirement.sh

COPY ./orders .

# run gunicorn
CMD gunicorn netology_pd_diplom.wsgi:application --bind 0.0.0.0:$PORT