# Taken from https://gist.github.com/jefftriplett/8ec40a937654f90a65d6886140215ec2
# with some modification

# docker python image
FROM python:alpine3.15

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

RUN apk update \
&& apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo

WORKDIR /src

RUN pip install --upgrade pip
COPY ./requirements-chill.txt .
RUN pip install -r requirements-chill.txt

COPY . .
RUN python bd_service/protoc/generate_pb.py
