FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /home/app/
COPY . $APP_HOME

ENTRYPOINT ["/home/app/entrypoint.sh"]
