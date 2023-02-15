# syntax=docker/dockerfile:1
ARG IMAGE_REPOSITORY=python
ARG IMAGE_TAG=3.6

FROM ${IMAGE_REPOSITORY}:${IMAGE_TAG}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
ADD requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt
ADD . /code/