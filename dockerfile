FROM python:3.10-slim-bullseye

RUN apt-get update \
  && pip install --no-cache-dir --upgrade pip\
  && pip install mysql-connector-python requests Flask jsonify

WORKDIR /python_base

# docker build -t python-flask-base .
# apt-get update && apt-get install -y curl
# apt-get update && apt-get install -y procps